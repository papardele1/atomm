"""Диагностика: отвечает ли Store77 серверу (напрямую или через прокси из переменной P)."""
import os
import re

import requests
from bs4 import BeautifulSoup

mode = os.environ.get("M", "direct")
proxy = os.environ.get("P", "")
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                "(KHTML, like Gecko) Chrome/130.0 Safari/537.36",
                  "Accept-Language": "ru-RU,ru;q=0.9"})
if proxy:
    s.proxies = {"http": proxy, "https": proxy}
for url in ["https://store77.net/", "https://store77.net/telefony_apple/"]:
    try:
        r = s.get(url, timeout=40)
        soup = BeautifulSoup(r.text, "lxml")
        n = len(soup.select(".wrap_list_prod .blocks_product"))
        title = (soup.title.string or "").strip()[:60] if soup.title else ""
        print(mode, url, r.status_code, len(r.text), "карточек:", n, "title:", title)
        if n == 0 and "telefony" in url:
            print("   начало ответа:", re.sub(r"\s+", " ", r.text[:400]))
    except Exception as e:  # noqa: BLE001
        print(mode, url, "ОШИБКА", repr(e)[:200])
