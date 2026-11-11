"""IndexNow для Яндекса: сообщает поисковику о новых и изменённых страницах сайта.

Протокол: https://yandex.ru/support/webmaster/indexnow/ — POST JSON {host, key, keyLocation, urlList}
на https://yandex.com/indexnow, до 10 000 URL за запрос. Ключ лежит в site/<KEY>.txt.

Логика (фоновый поток в api.py):
- первый проход через ~2 минуты после старта, дальше раз в 6 часов;
- URL берутся из sitemap (страницы с товарами в наличии);
- новые URL (ещё ни разу не отправленные) уходят сразу;
- разделы, подборки, модели и гайды (их немного, на них меняются цены и наличие) — не чаще раза в сутки;
- остальные (товары /p/, страницы памяти) повторно — раз в 7 дней.
Состояние — JSON рядом с базой заказов (/data), итог последнего прохода — в /api/health.
"""
import json
import os
import re
import threading
import time

import requests

KEY = os.environ.get("ATOMM_INDEXNOW_KEY", "bb0de25ef63c81dc9b8e2c0ce48cb02a")
HOST = "atomm.store"
BASE = f"https://{HOST}"
ENDPOINT = os.environ.get("ATOMM_INDEXNOW_URL", "https://yandex.com/indexnow")
BATCH = 10000
DAY = 86400
HUB_EVERY = DAY
REST_EVERY = 7 * DAY

status = {"enabled": os.environ.get("ATOMM_INDEXNOW", "1") != "0"}


def _is_hub(u):
    path = u[len(BASE):]
    return path.startswith("/guides/") or (path.startswith("/catalog/") and path.count("/") <= 3) or path == "/"


def due(urls, sent, now):
    """URL, которые пора отправить: новые сразу, хабы — раз в сутки, остальные — раз в неделю."""
    out = []
    for u in urls:
        t = sent.get(u)
        if t is None or now - t >= (HUB_EVERY if _is_hub(u) else REST_EVERY) - 600:
            out.append(u)
    return out


def submit(urls, post=None):
    """Отправляет URL пачками; возвращает (сколько принято, последний HTTP-код)."""
    post = post or requests.post
    ok, code = 0, None
    for i in range(0, len(urls), BATCH):
        chunk = urls[i:i + BATCH]
        r = post(ENDPOINT, json={"host": HOST, "key": KEY, "keyLocation": f"{BASE}/{KEY}.txt", "urlList": chunk},
                 headers={"Content-Type": "application/json; charset=utf-8"}, timeout=60)
        code = r.status_code
        if code not in (200, 202):
            break
        ok += len(chunk)
    return ok, code


def run_once(sitemap_xml, state_path, now=None, post=None):
    now = now or time.time()
    urls = re.findall(r"<loc>([^<]+)</loc>", sitemap_xml or "")
    urls = [u.replace("&amp;", "&") for u in urls if u.startswith(BASE)]
    if not urls:
        return {"at": int(now), "skipped": "пустой sitemap"}
    try:
        with open(state_path, encoding="utf-8") as f:
            sent = json.load(f)
    except (OSError, ValueError):
        sent = {}
    todo = due(urls, sent, now)
    res = {"at": int(now), "urls": len(urls), "due": len(todo)}
    if todo:
        ok, code = submit(todo, post)
        res.update(sent=ok, http=code)
        for u in todo[:ok]:
            sent[u] = now
        live = set(urls)
        sent = {u: t for u, t in sent.items() if u in live or now - t < 30 * DAY}
        tmp = f"{state_path}.{os.getpid()}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(sent, f)
        os.replace(tmp, state_path)
    return res


def start(get_sitemap, state_path, first_delay=120, every=6 * 3600):
    """Фоновый поток: get_sitemap() -> XML sitemap или None (каталог ещё не загружен)."""
    if not status["enabled"]:
        return

    def loop():
        time.sleep(first_delay)
        while True:
            try:
                status["last"] = run_once(get_sitemap(), state_path)
            except Exception as e:  # сеть, Яндекс недоступен — попробуем на следующем круге
                status["last"] = {"at": int(time.time()), "error": repr(e)[:200]}
            time.sleep(every)

    threading.Thread(target=loop, daemon=True).start()
