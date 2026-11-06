"""API приёма заказов ATOMM.

POST /api/order — проверяет заказ по актуальному catalog.json (цены считаются на сервере,
не берутся из браузера), сохраняет в SQLite и отправляет уведомление в Telegram.
GET  /api/health — проверка работы.
В Docker-режиме (ATOMM_SITE задан) также отдаёт сам сайт и catalog.json.
"""
import json
import os
import re
import sqlite3
import threading
import time
from collections import defaultdict, deque

import shutil

import requests
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

CATALOG = os.environ.get("ATOMM_CATALOG", "/var/www/atomm/catalog.json")
DB = os.environ.get("ATOMM_DB", "/var/lib/atomm/orders.db")
TG_TOKEN = os.environ.get("TG_TOKEN", "")
TG_CHAT = os.environ.get("TG_CHAT", "")
SITE = os.environ.get("ATOMM_SITE", "")  # папка со статикой сайта (Docker-режим)
CHAT_FILE = os.path.join(os.path.dirname(DB) or ".", "tg_chat")

# каталог: при первом запуске берём снимок из образа, дальше его обновляет парсер
if SITE and not os.path.exists(CATALOG):
    os.makedirs(os.path.dirname(CATALOG), exist_ok=True)
    shutil.copy(os.path.join(SITE, "catalog.json"), CATALOG)
os.makedirs(os.path.dirname(DB) or ".", exist_ok=True)


def _clean_catalog():
    """Убирает из уже собранного каталога товары, которые мы не продаём (правила в catalog_lib)."""
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    import catalog_lib
    try:
        with open(CATALOG, encoding="utf-8") as f:
            d = json.load(f)
    except (OSError, ValueError):
        return
    keep = [i for i in d["items"] if not catalog_lib.is_excluded(i[4], d["subs"][i[3]])]
    if len(keep) == len(d["items"]):
        return
    brands = sorted({d["brands"][i[2]] for i in keep if i[2] >= 0})
    subs = sorted({d["subs"][i[3]] for i in keep})
    bi = {b: k for k, b in enumerate(brands)}
    si = {x: k for k, x in enumerate(subs)}
    d["items"] = [[i[0], i[1], bi[d["brands"][i[2]]] if i[2] >= 0 else -1, si[d["subs"][i[3]]]] + i[4:] for i in keep]
    d["brands"], d["subs"] = brands, subs
    catalog_lib.write_atomic(d, CATALOG)


_clean_catalog()

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
_lock = threading.Lock()
_cat = {"mtime": 0, "by_id": {}}
_hits = defaultdict(deque)


def catalog():
    m = os.path.getmtime(CATALOG)
    if m != _cat["mtime"]:
        with open(CATALOG, encoding="utf-8") as f:
            d = json.load(f)
        _cat["by_id"] = {it[0]: {"name": it[4], "price": it[5], "stock": it[6]} for it in d["items"]}
        _cat["mtime"] = m
    return _cat["by_id"]


def db():
    con = sqlite3.connect(DB)
    con.execute("""create table if not exists orders(
        id integer primary key autoincrement, created text, name text, phone text, addr text,
        pay text, total integer, items text, ip text)""")
    return con


class Line(BaseModel):
    id: str = Field(max_length=20)
    qty: int = Field(ge=1, le=20)


class Order(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=5, max_length=30)
    addr: str = Field(default="", max_length=400)
    pay: str
    consent: bool
    items: list[Line] = Field(min_length=1, max_length=50)


def err(msg, code=400):
    return JSONResponse({"ok": False, "error": msg}, status_code=code)


def limited(ip):
    q = _hits[ip]
    now = time.time()
    while q and now - q[0] > 600:
        q.popleft()
    q.append(now)
    return len(q) > 5  # не больше 5 заказов за 10 минут с одного адреса


def chat_id():
    """Чат для уведомлений: из настроек, иначе — тот, кто первым написал боту /start."""
    if TG_CHAT:
        return TG_CHAT
    try:
        with open(CHAT_FILE) as f:
            return f.read().strip()
    except OSError:
        return ""


# --- Telegram: из российских дата-центров связь с api.telegram.org нестабильна,
# поэтому все сообщения идут через очередь в SQLite и повторяются до доставки.
_wake = threading.Event()
WELCOME_FLAG = os.path.join(os.path.dirname(DB) or ".", "tg_welcome_sent")


def _outbox_db():
    con = sqlite3.connect(DB, timeout=10)
    con.execute("""create table if not exists outbox(
        id integer primary key autoincrement, created text, text text,
        sent integer default 0, tries integer default 0, last_error text)""")
    return con


def notify(text):
    with _lock:
        con = _outbox_db()
        con.execute("insert into outbox(created, text) values(?, ?)", (time.strftime("%Y-%m-%d %H:%M:%S"), text))
        con.commit()
        con.close()
    _wake.set()


def _tg(method, **kw):
    return requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/{method}", json=kw, timeout=(6, 30)).json()


def _sender():
    while True:
        _wake.wait(20)
        _wake.clear()
        chat = chat_id()
        if not (TG_TOKEN and chat):
            continue
        con = _outbox_db()
        rows = con.execute("select id, text from outbox where sent = 0 order by id limit 20").fetchall()
        for oid, text in rows:
            try:
                r = _tg("sendMessage", chat_id=chat, text=text)
                if r.get("ok"):
                    con.execute("update outbox set sent = 1 where id = ?", (oid,))
                elif r.get("error_code") in (400, 403):  # чат недоступен — не повторяем бесконечно
                    con.execute("update outbox set sent = -1, last_error = ? where id = ?", (str(r)[:300], oid))
                else:
                    con.execute("update outbox set tries = tries + 1, last_error = ? where id = ?", (str(r)[:300], oid))
            except Exception as e:  # сеть: попробуем снова на следующем круге
                con.execute("update outbox set tries = tries + 1, last_error = ? where id = ?", (repr(e)[:300], oid))
                con.commit()
                break
            con.commit()
        con.close()


def _watch_start():
    """Ждёт /start от владельца, чтобы узнать чат для заказов (если TG_CHAT не задан)."""
    offset = None
    while TG_TOKEN and not chat_id():
        try:
            r = requests.get(f"https://api.telegram.org/bot{TG_TOKEN}/getUpdates",
                             params={"timeout": 25, "offset": offset}, timeout=(6, 35)).json()
            for u in r.get("result", []):
                offset = u["update_id"] + 1
                m = u.get("message") or {}
                if (m.get("text") or "").startswith("/start"):
                    with open(CHAT_FILE, "w") as f:
                        f.write(str(m["chat"]["id"]))
                    break
        except Exception:
            time.sleep(10)
    if TG_TOKEN and chat_id() and not os.path.exists(WELCOME_FLAG):
        notify("✅ ATOMM подключён. Сюда будут приходить новые заказы.")
        open(WELCOME_FLAG, "w").close()


threading.Thread(target=_sender, daemon=True).start()
threading.Thread(target=_watch_start, daemon=True).start()


def rub(n):
    return f"{n:,}".replace(",", " ") + " ₽"


@app.get("/api/health")
def health():
    out = {"ok": True, "items": len(catalog()), "telegram": bool(TG_TOKEN and chat_id())}
    try:
        con = _outbox_db()
        out["tg_queue"] = con.execute("select count(*) from outbox where sent = 0").fetchone()[0]
        con.close()
    except sqlite3.Error:
        pass
    return out


@app.post("/api/order")
def order(o: Order, request: Request):
    ip = request.headers.get("x-real-ip") or request.client.host
    if limited(ip):
        return err("Слишком много заказов подряд. Попробуйте позже.", 429)
    if not o.consent:
        return err("Нужно согласие на обработку персональных данных.")
    if o.pay == "card":
        return err("Оплата картой по техническим причинам временно недоступна. Выберите оплату наличными при получении.")
    if o.pay != "cash":
        return err("Неизвестный способ оплаты.")
    digits = re.sub(r"\D", "", o.phone)
    if len(digits) < 10:
        return err("Проверьте номер телефона.")
    cat = catalog()
    lines, total = [], 0
    for ln in o.items:
        it = cat.get(ln.id)
        if not it:
            return err("Один из товаров больше не продаётся. Обновите корзину.")
        if not it["stock"] or not it["price"]:
            return err(f"Нет в наличии: {it['name']}")
        lines.append({"id": ln.id, "name": it["name"], "qty": ln.qty, "price": it["price"]})
        total += it["price"] * ln.qty
    with _lock:
        con = db()
        cur = con.execute("insert into orders(created,name,phone,addr,pay,total,items,ip) values(?,?,?,?,?,?,?,?)",
                          (time.strftime("%Y-%m-%d %H:%M:%S"), o.name.strip(), o.phone.strip(), o.addr.strip(),
                           o.pay, total, json.dumps(lines, ensure_ascii=False), ip))
        con.commit()
        no = cur.lastrowid
        con.close()
    body = "\n".join(f"• {l['name']} × {l['qty']} — {rub(l['price'] * l['qty'])}" for l in lines)
    notify(f"🛒 Новый заказ №{no}\n\n{body}\n\nИтого: {rub(total)}\nОплата: наличными при получении\n\n"
           f"Имя: {o.name}\nТелефон: {o.phone}\nАдрес: {o.addr or '—'}")
    return {"ok": True, "order": no, "total": total}


# --- статика сайта (Docker-режим): должна подключаться последней ---
if SITE:
    @app.get("/catalog.json")
    def catalog_file():
        return FileResponse(CATALOG, media_type="application/json", headers={"Cache-Control": "no-cache"})

    app.mount("/", StaticFiles(directory=SITE, html=True), name="site")
