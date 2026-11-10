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
DELIVERY_PRICE = int(os.environ.get("ATOMM_DELIVERY_PRICE", "1000"))
DELIVERY_CUTOFF_HOUR = 15          # заказ до 15:00 по Москве — доставка в тот же день
DELIVERY_WINDOW = "с 17:00 до 22:00"
PICKUP_ADDR = "Москва, Багратионовский проезд, 7к2"
MSK = __import__("datetime").timezone(__import__("datetime").timedelta(hours=3))


def delivery_day(now=None):
    """'сегодня' или 'завтра' + дата, по московскому времени."""
    import datetime as dt
    now = now or dt.datetime.now(MSK)
    day = now.date() if now.hour < DELIVERY_CUTOFF_HOUR else now.date() + dt.timedelta(days=1)
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября",
              "октября", "ноября", "декабря"]
    word = "сегодня" if day == now.date() else "завтра"
    return f"{word}, {day.day} {months[day.month - 1]}"


CHAT_FILE = os.path.join(os.path.dirname(DB) or ".", "tg_chat")

# каталог: при первом запуске берём снимок из образа, дальше его обновляет парсер
if SITE and not os.path.exists(CATALOG):
    os.makedirs(os.path.dirname(CATALOG), exist_ok=True)
    shutil.copy(os.path.join(SITE, "catalog.json"), CATALOG)
os.makedirs(os.path.dirname(DB) or ".", exist_ok=True)


def _clean_catalog():
    """Приводит уже собранный каталог к текущим правилам: исключения (catalog_lib) и порядок по старшинству."""
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    import catalog_lib
    try:
        with open(CATALOG, encoding="utf-8") as f:
            d = json.load(f)
    except (OSError, ValueError):
        return
    secs, brands, subs = d["sections"], d["brands"], d["subs"]
    keep = [i for i in d["items"] if not catalog_lib.is_excluded(i[4], subs[i[3]])
            and secs[i[1]] in catalog_lib.SECTIONS]
    sec_idx = {n: k for k, n in enumerate(catalog_lib.SECTIONS)}
    rows = [[i[0], sec_idx[secs[i[1]]], brands[i[2]] if i[2] >= 0 else "", subs[i[3]]] + i[4:] for i in keep]
    catalog_lib.resolve_subs(rows, lambda r: r[1], lambda r: r[4], lambda r: r[3], lambda r, v: r.__setitem__(3, v))
    for r in rows:
        r[4] = catalog_lib.sim_named(r[4], r[3])
    catalog_lib.seniority_sort(rows, lambda r: (r[1], r[2], r[4], r[5]))
    new_brands = sorted({r[2] for r in rows if r[2]})
    new_subs = catalog_lib.order_subs(r[3] for r in rows)
    bi = {b: k for k, b in enumerate(new_brands)}
    si = {x: k for k, x in enumerate(new_subs)}
    items = [[r[0], r[1], bi[r[2]] if r[2] else -1, si[r[3]]] + r[4:] for r in rows]
    if items == d["items"] and d["sections"] == catalog_lib.SECTIONS and new_subs == subs:
        return
    d.update(sections=catalog_lib.SECTIONS, brands=new_brands, subs=new_subs, items=items)
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
    method: str = "courier"
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


TG_PROXY = os.environ.get("TG_PROXY", "").strip()
_route = {"via": "direct", "until": 0.0}  # какой путь сработал последним; держим его 10 минут


def _tg_once(method, via, kw, read=10):
    proxies = {"https": TG_PROXY, "http": TG_PROXY} if via == "proxy" else None
    return requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/{method}", json=kw,
                         timeout=(3, read), proxies=proxies).json()


def _tg(method, read=10, **kw):
    """Связь с Telegram с сервера нестабильна: обычный ответ — 0,2 с, но часть соединений «зависает».
    Поэтому короткий таймаут и быстрые повторы, чередуя путь: сначала тот, что сработал последним,
    затем другой (напрямую ↔ через прокси). До 9 попыток, в худшем случае ~40 секунд; при неудаче очередь повторит через 5 секунд."""
    first = _route["via"] if time.time() < _route["until"] else "direct"
    other = "proxy" if first == "direct" else "direct"
    # Замер с сервера: напрямую проходит ~половина попыток, мобильный прокси до Telegram пока не доходит,
    # поэтому основной путь повторяем чаще, а запасной вставляем через раз.
    order = [first, first, other] * 3 if TG_PROXY else ["direct"] * 8
    err = None
    for i, via in enumerate(order):
        try:
            r = _tg_once(method, via, kw, read)
            _route.update(via=via, until=time.time() + 600)
            r["_via"] = via
            return r
        except requests.RequestException as e:
            err = e
            time.sleep(0.3)
    raise err


def _sender():
    pending = False
    while True:
        _wake.wait(5 if pending else 20)
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
                    con.execute("update outbox set sent = 1, last_error = ? where id = ?",
                                ("доставлено: " + ("через прокси" if r.get("_via") == "proxy" else "напрямую"), oid))
                elif r.get("error_code") in (400, 403):  # чат недоступен — не повторяем бесконечно
                    con.execute("update outbox set sent = -1, last_error = ? where id = ?", (str(r)[:300], oid))
                else:
                    con.execute("update outbox set tries = tries + 1, last_error = ? where id = ?", (str(r)[:300], oid))
            except Exception as e:  # сеть: попробуем снова на следующем круге
                con.execute("update outbox set tries = tries + 1, last_error = ? where id = ?", (repr(e)[:300], oid))
                con.commit()
                break
            con.commit()
        pending = bool(con.execute("select 1 from outbox where sent = 0 limit 1").fetchone())
        con.close()


def _watch_start():
    """Ждёт /start от владельца, чтобы узнать чат для заказов (если TG_CHAT не задан)."""
    offset = None
    while TG_TOKEN and not chat_id():
        try:
            r = _tg("getUpdates", read=30, timeout=20, offset=offset)
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
    pickup = o.method == "pickup"
    if not pickup and len(o.addr.strip()) < 5:
        return err("Укажите адрес доставки.")
    addr = f"САМОВЫВОЗ ({PICKUP_ADDR})" if pickup else o.addr.strip()
    dprice = 0 if pickup else DELIVERY_PRICE
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
    goods = total
    total += dprice
    when = "самовывоз, время согласуем по телефону" if pickup else f"{delivery_day()}, {DELIVERY_WINDOW}"
    with _lock:
        con = db()
        cur = con.execute("insert into orders(created,name,phone,addr,pay,total,items,ip) values(?,?,?,?,?,?,?,?)",
                          (time.strftime("%Y-%m-%d %H:%M:%S"), o.name.strip(), o.phone.strip(), addr,
                           o.pay, total, json.dumps(lines, ensure_ascii=False), ip))
        con.commit()
        no = cur.lastrowid
        con.close()
    body = "\n".join(f"• {l['name']} × {l['qty']} — {rub(l['price'] * l['qty'])}" for l in lines)
    dl = "🏬 САМОВЫВОЗ (бесплатно)\nСогласовать время с покупателем" if pickup else f"Доставка: {rub(dprice)}\nДоставить: {when}"
    notify(f"🛒 Новый заказ №{no}\n\n{body}\n\nТовары: {rub(goods)}\n{dl}\n"
           f"Итого: {rub(total)}\nОплата: наличными при получении\n\n"
           f"Имя: {o.name}\nТелефон: {o.phone}\nАдрес: {addr}")
    return {"ok": True, "order": no, "total": total, "delivery": dprice, "when": when, "pickup": pickup}


# --- статика сайта (Docker-режим): должна подключаться последней ---
if SITE:
    @app.get("/catalog.json")
    def catalog_file():
        return FileResponse(CATALOG, media_type="application/json", headers={"Cache-Control": "no-cache"})

    IMG_DIR = os.environ.get("ATOMM_IMG", os.path.join(os.path.dirname(CATALOG), "img"))
    os.makedirs(IMG_DIR, exist_ok=True)

    @app.get("/img/index.json")
    def img_index():
        p = os.path.join(IMG_DIR, "index.json")
        if not os.path.exists(p):
            return JSONResponse({}, headers={"Cache-Control": "no-cache"})
        return FileResponse(p, media_type="application/json", headers={"Cache-Control": "no-cache"})

    class _ImgFiles(StaticFiles):  # фото неизменны (имя = хэш), кэшируем надолго
        async def get_response(self, path, scope):
            r = await super().get_response(path, scope)
            if r.status_code == 200:
                r.headers["Cache-Control"] = "public, max-age=2592000, immutable"
            return r

    import feed as _feed
    from fastapi.responses import HTMLResponse, Response

    @app.get("/feed.yml")
    def feed_yml():
        x = _feed.yml(CATALOG, IMG_DIR)
        if not x:
            return JSONResponse({"ok": False}, status_code=503)
        return Response(x, media_type="application/xml; charset=utf-8", headers={"Cache-Control": "no-cache"})

    import seo as _seo
    from fastapi.responses import RedirectResponse

    def _m():
        return _seo.model(CATALOG, IMG_DIR)

    def _404():
        return HTMLResponse(_seo.not_found(_m()), status_code=404)

    _HTML_HDR = {"Cache-Control": "public, max-age=300"}

    @app.get("/p/{iid}")
    def product(iid: str):
        m = _m()
        h = _seo.page_product(m, iid) if m else None
        return HTMLResponse(h, headers=_HTML_HDR) if h else _404()

    @app.get("/sitemap.xml")
    def sitemap_xml():
        m = _m()
        if not m:
            return FileResponse(os.path.join(SITE, "sitemap.xml"), media_type="application/xml")
        return Response(_seo.sitemap(m), media_type="application/xml; charset=utf-8", headers=_HTML_HDR)

    def _redir(path, request):
        q = request.url.query
        return RedirectResponse(path + ("?" + q if q else ""), status_code=301)

    @app.get("/catalog")
    def catalog_noslash(request: Request):
        return _redir("/catalog/", request)

    @app.get("/catalog/")
    def catalog_hub():
        m = _m()
        return HTMLResponse(_seo.page_hub(m), headers=_HTML_HDR) if m else _404()

    @app.get("/catalog/{slug}")
    def catalog_slug_noslash(slug: str, request: Request):
        return _redir(f"/catalog/{slug}/", request)

    @app.get("/catalog/{slug}/")
    def catalog_page(slug: str):
        m = _m()
        h = _seo.render(m, slug) if m else None
        return HTMLResponse(h, headers=_HTML_HDR) if h else _404()

    @app.get("/catalog/{slug}/{sub}")
    def catalog_sub_noslash(slug: str, sub: str, request: Request):
        return _redir(f"/catalog/{slug}/{sub}/", request)

    @app.get("/catalog/{slug}/{sub}/")
    def catalog_subpage(slug: str, sub: str):
        m = _m()
        h = _seo.render(m, slug, sub) if m else None
        return HTMLResponse(h, headers=_HTML_HDR) if h else _404()

    @app.get("/guides/{slug}")
    def guide_noslash(slug: str, request: Request):
        return _redir(f"/guides/{slug}/", request)

    @app.get("/guides/{slug}/")
    def guide_page(slug: str):
        m = _m()
        h = _seo.page_guide(m, slug) if m else None
        return HTMLResponse(h, headers=_HTML_HDR) if h else _404()

    @app.get("/catalog.html")
    def catalog_html():
        with open(os.path.join(SITE, "catalog.html"), encoding="utf-8") as f:
            h = f.read()
        m = _m()
        if m:
            h = h.replace("<!--SEO_LINKS-->", _seo.catalog_links(m))
        return HTMLResponse(h, headers={"Cache-Control": "no-cache"})

    @app.get("/index.html")
    def index_html(request: Request):
        return _redir("/", request)

    app.mount("/img", _ImgFiles(directory=IMG_DIR), name="img")
    app.mount("/", StaticFiles(directory=SITE, html=True), name="site")
