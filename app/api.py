"""API приёма заказов ATOMM.

POST /api/order — проверяет заказ по актуальному catalog.json (цены считаются на сервере,
не берутся из браузера), сохраняет в SQLite и отправляет уведомление в Telegram.
GET  /api/health — проверка работы.
"""
import json
import os
import re
import sqlite3
import threading
import time
from collections import defaultdict, deque

import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

CATALOG = os.environ.get("ATOMM_CATALOG", "/var/www/atomm/catalog.json")
DB = os.environ.get("ATOMM_DB", "/var/lib/atomm/orders.db")
TG_TOKEN = os.environ.get("TG_TOKEN", "")
TG_CHAT = os.environ.get("TG_CHAT", "")

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


def notify(text):
    if not (TG_TOKEN and TG_CHAT):
        return
    try:
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                      json={"chat_id": TG_CHAT, "text": text}, timeout=10)
    except requests.RequestException:
        pass


def rub(n):
    return f"{n:,}".replace(",", " ") + " ₽"


@app.get("/api/health")
def health():
    return {"ok": True, "items": len(catalog())}


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
