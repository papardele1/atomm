"""Цены конкурента для отдельных моделей.

iPhone 18 Pro Max: берём цены с technolab.ru; наша цена — меньшая из двух: обычная (Store77) или technolab −100 ₽
(решение владельца, 10.11.2026).
Сбор — в каждом цикле парсера (раз в 4 часа); результат лежит в /www/competitor/technolab.json,
а применяется при сборке каталога (catalog_lib.build) и сразу к текущему catalog.json (apply_to_catalog).
"""
import json
import logging
import os
import re
import time

import requests

log = logging.getLogger("competitor")

DIR = os.path.join(os.path.dirname(os.environ.get("ATOMM_CATALOG", "/www/catalog.json")), "competitor")
FILE = os.path.join(DIR, "technolab.json")
MAX_AGE = 3 * 86400  # старше трёх дней — не применяем (если сайт перестал отдаваться)
UNDERCUT = 100

TARGETS = {  # наш подраздел → страница конкурента
    "Apple iPhone 18 Pro Max": "https://technolab.ru/catalog/smartfony/apple_3/iphone_18_pro_max?sorting=price-asc",
}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/130.0 Safari/537.36", "Accept-Language": "ru-RU,ru"}
_ROW = re.compile(r'\\"title\\":\\"(Телефон Apple iPhone[^"\\]+)\\".{0,1500}?\\"discounted_price\\":(null|\\"[\d ]+\\"|\d+),'
                  r'\\"price\\":\\"([\d ]+)\\"', re.S)


def _num(s):
    s = re.sub(r"\D", "", s or "")
    return int(s) if s else 0


def _page(url, n):
    if n == 1:
        return url
    sep = "&" if "?" in url else "?"
    return [f"{url}{sep}page={n}", f"{url}{sep}PAGEN_1={n}"]


def fetch(url):
    """Все товары подраздела конкурента: {название: цена}. Перебирает страницы, пока появляются новые товары."""
    out = {}
    for n in range(1, 6):
        variants = _page(url, n)
        got_new = False
        for u in ([variants] if isinstance(variants, str) else variants):
            r = requests.get(u, headers=HEADERS, timeout=40)
            r.raise_for_status()
            rows = _ROW.findall(r.text)
            new = 0
            for title, disc, price in rows:
                p = _num(disc) if disc != "null" else 0
                p = p or _num(price)
                if title not in out and p > 1000:
                    out[title] = p
                    new += 1
            if new:
                got_new = True
                break
        if not got_new:
            break
    return out


def key_competitor(title):
    """«Телефон Apple iPhone 18 Pro Max 256Gb E-Sim (Silver)» → ('256', 'esim', 'silver')."""
    m = re.search(r"(\d+)\s*(gb|tb)", title, re.I)
    if not m:
        return None
    mem = str(int(m.group(1)) * (1024 if m.group(2).lower() == "tb" else 1))
    sim = "esim" if re.search(r"e-?sim", title, re.I) else "nano"
    if re.search(r"dual|2\s*sim", title, re.I):
        sim = "dual"
    c = re.findall(r"\(([A-Za-z][A-Za-z \-]+)\)", title)
    return (mem, sim, c[-1].strip().lower()) if c else None


def key_ours(name):
    """Наше название → тот же ключ. eSim (электронная …) — только eSIM; Dual sim — две SIM; иначе nano-SIM + eSIM."""
    m = re.search(r"(\d+)\s*(ГБ|ТБ|GB|TB)", name, re.I)
    if not m:
        return None
    mem = str(int(m.group(1)) * (1024 if m.group(2).upper() in ("ТБ", "TB") else 1))
    if re.search(r"dual\s*sim|две\s*sim", name, re.I):
        sim = "dual"
    elif re.search(r"esim\s*\(электрон", name, re.I):
        sim = "esim"
    else:
        sim = "nano"
    c = re.findall(r"\(([A-Za-z][A-Za-z \-]+)\)", name)
    return (mem, sim, c[-1].strip().lower()) if c else None


def collect():
    """Скачать цены по всем TARGETS и сохранить. Ошибка одной страницы не трогает прошлые данные."""
    try:
        with open(FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = {}
    for sub, url in TARGETS.items():
        try:
            prices = fetch(url)
        except Exception as e:  # сеть/защита — оставляем прошлые цены
            log.warning("technolab %s: %s", sub, e)
            continue
        if len(prices) < 4:
            log.warning("technolab %s: найдено только %s товаров — не обновляю", sub, len(prices))
            continue
        data[sub] = {"t": int(time.time()), "url": url, "prices": prices}
        log.info("technolab %s: %s товаров", sub, len(prices))
    os.makedirs(DIR, exist_ok=True)
    tmp = FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    os.replace(tmp, FILE)
    return data


def overrides():
    """{подраздел: {ключ: наша цена}} из свежих данных конкурента."""
    try:
        with open(FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    out = {}
    now = time.time()
    for sub, d in data.items():
        if sub not in TARGETS or now - d.get("t", 0) > MAX_AGE:
            continue
        m = {}
        for title, p in d["prices"].items():
            k = key_competitor(title)
            if k:
                m[k] = min(m.get(k, p - UNDERCUT), p - UNDERCUT)
        out[sub] = m
    return out


def apply(rows, sub_of, name_of, set_price, price_of=None):
    """Цена = меньшая из двух: наша обычная или цена конкурента −100 ₽. Возвращает число совпавших товаров."""
    ov = overrides()
    if not ov:
        return 0
    n = 0
    for r in rows:
        m = ov.get(sub_of(r))
        if not m:
            continue
        k = key_ours(name_of(r))
        if k in m:
            cur = price_of(r) if price_of else 0
            set_price(r, min(cur, m[k]) if cur else m[k])  # меньшая из двух: наша обычная или конкурент −100 ₽
            n += 1
    return n


def apply_to_catalog(path):
    """Сразу обновить уже собранный catalog.json (без ожидания следующего прохода парсера)."""
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    subs = d["subs"]
    before = {it[0]: it[5] for it in d["items"]}
    n = apply(d["items"], lambda it: subs[it[3]], lambda it: it[4], lambda it, p: it.__setitem__(5, p), lambda it: it[5])
    changed = [it for it in d["items"] if before[it[0]] != it[5]]
    if changed:
        import catalog_lib
        catalog_lib.write_atomic(d, path)
    return n, changed, before
