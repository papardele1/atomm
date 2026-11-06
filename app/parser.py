"""Парсер цен Store77 → catalog.json для сайта ATOMM.

Запускается по таймеру systemd (atomm-parser.timer). Обходит все разделы каталога
постранично, собирает товары и цены, считает цены ATOMM (−0,5 %) и атомарно
заменяет catalog.json. Если собрано заметно меньше товаров, чем в прошлый раз,
файл не заменяется (защита от частичного сбора при блокировке/сбое).
"""
import json
import logging
import os
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(__file__))
import catalog_lib  # noqa: E402

BASE = "https://store77.net"
OUT = os.environ.get("ATOMM_CATALOG", "/var/www/atomm/catalog.json")
PROXY = os.environ.get("ATOMM_PROXY") or None  # например http://user:pass@host:port
WORKERS = int(os.environ.get("ATOMM_PARSER_WORKERS", "3"))
MIN_RATIO = 0.7
TOPS = ["/telefony_apple/", "/planshety/", "/umniye_chasy_i_braslety/", "/audio/", "/telefony_xiaomi/",
        "/produktsiya_huawei/", "/kompyuternaya_tekhnika/", "/igrovye_pristavki/", "/aksessuary/",
        "/utsenennye_tovary/"]
SKIP = {"/favorites", "/personal/cart/", "/search/"}

log = logging.getLogger("atomm-parser")
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/130.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9",
})
if PROXY:
    session.proxies = {"http": PROXY, "https": PROXY}


def get(url, tries=3):
    for i in range(tries):
        try:
            r = session.get(url, timeout=40)
            if r.status_code == 200:
                return r.text
            log.warning("HTTP %s %s", r.status_code, url)
        except requests.RequestException as e:
            log.warning("ошибка %s: %s", url, e)
        time.sleep(3 * (i + 1))
    return None


def discover_categories():
    html = get(BASE + "/")
    if not html:
        raise SystemExit("Главная Store77 недоступна")
    soup = BeautifulSoup(html, "lxml")
    cats = {}
    for a in soup.select("a[href]"):
        h = a["href"].split("?")[0].split("#")[0]
        if h.startswith("/") and len([p for p in h.split("/") if p]) == 1 and h not in SKIP and h not in cats:
            cats[h] = " ".join(a.get_text().split())[:60]
    return cats


def num(text):
    digits = "".join(ch for ch in (text or "") if ch.isdigit())
    return int(digits) if digits else None


def parse_page(html):
    soup = BeautifulSoup(html, "lxml")
    out = []
    for c in soup.select(".wrap_list_prod .blocks_product"):
        name_a = next((a for a in c.select("a[href]") if len(a.get_text(strip=True)) > 20), None)
        if not name_a:
            continue
        pe = c.select_one(".bp_text_price")
        btn = c.select_one(".link_but")
        out.append(dict(url=name_a["href"].split("?")[0], name=" ".join(name_a.get_text().split()),
                        price=num(pe.get_text() if pe else ""),
                        in_stock="корзин" in (btn.get_text().lower() if btn else "")))
    return out


class Store:
    def __init__(self):
        self.prods = {}

    def add(self, cards, cat):
        new = 0
        for p in cards:
            rec = self.prods.get(p["url"])
            if rec:
                if cat not in rec["cats"]:
                    rec["cats"].append(cat)
                continue
            p["cats"] = [cat]
            self.prods[p["url"]] = p
            new += 1
        return new


def crawl_cat(store, cat, force):
    html = get(BASE + cat)
    if not html:
        return
    first = parse_page(html)
    new = store.add(first, cat)
    if not first or len(first) < 24 or not (force or new):
        return
    for pg in range(2, 400):
        time.sleep(random.uniform(0.4, 1.0))
        html = get(f"{BASE}{cat}?PAGEN_1={pg}")
        if not html:
            break
        cards = parse_page(html)
        if not cards or cards[0]["url"] == first[0]["url"]:
            break
        store.add(cards, cat)
        if len(cards) < 24:
            break


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    t0 = time.time()
    cats = discover_categories()
    rest = [c for c in cats if c not in TOPS]
    store = Store()
    with ThreadPoolExecutor(WORKERS) as ex:
        list(ex.map(lambda c: crawl_cat(store, c, True), TOPS))
        list(ex.map(lambda c: crawl_cat(store, c, False), rest))
    products = []
    for url, p in store.prods.items():
        leaf = next((c for c in p["cats"] if c not in TOPS), p["cats"][0])
        top = next((c for c in p["cats"] if c in TOPS), "")
        products.append(dict(url=url, name=p["name"], price=p["price"], in_stock=p["in_stock"],
                             sub_name=cats.get(leaf, leaf.strip("/")), top=top))
    data = catalog_lib.build(products)
    n = len(data["items"])
    prev = 0
    try:
        with open(OUT, encoding="utf-8") as f:
            prev = len(json.load(f)["items"])
    except Exception:
        pass
    if prev and n < prev * MIN_RATIO:
        log.error("Собрано %s товаров против %s в прошлый раз — каталог НЕ обновлён", n, prev)
        sys.exit(2)
    catalog_lib.write_atomic(data, OUT)
    log.info("Готово: %s товаров (было %s) за %.0f с", n, prev, time.time() - t0)


if __name__ == "__main__":
    main()
