"""Товарный YML-фид для Яндекса (/feed.yml). Страницы товаров и разделов — в seo.py."""
import html
import json
import os
import re
import time

BASE = "https://atomm.store"
SHOP = "ATOMM"
COMPANY = "ИП Головин Руслан Андреевич"
PICKUP = "Москва, Багратионовский проезд, 7к2"
DELIVERY_COST = 1000

_cache = {"key": None, "data": None}


def _load(catalog_path, img_dir):
    try:
        m1 = os.path.getmtime(catalog_path)
        idx_path = os.path.join(img_dir, "index.json")
        m2 = os.path.getmtime(idx_path) if os.path.exists(idx_path) else 0
    except OSError:
        return None
    key = (m1, m2)
    if _cache["key"] != key:
        with open(catalog_path, encoding="utf-8") as f:
            d = json.load(f)
        idx = {}
        if m2:
            with open(idx_path, encoding="utf-8") as f:
                idx = json.load(f)
        by_id = {it[0]: it for it in d["items"]}
        _cache.update(key=key, data=(d, idx, by_id, None))
    return _cache["data"]


_ACC_SEC = "Аксессуары"
_ACC_SUB = re.compile(r"аксессуар|чехл|кабел|заряд|ремеш|плёнк|пленк|стекл|^для\s", re.I)


def sub_section(sub, secs):
    """Раздел подраздела по большинству его товаров (secs — разделы товаров в порядке каталога).
    Подраздел-тёзка раздела («Аксессуары») всегда относится к своему разделу. Раздел «Аксессуары» не перетягивает
    подразделы устройств («Пылесосы Dyson», «Товары для дома»): в источнике туда попадают сами устройства.
    Используется и сайтом (seo.py), и фидом — чтобы категории совпадали."""
    cnt, first = {}, {}
    for k, sec in enumerate(secs):
        cnt[sec] = cnt.get(sec, 0) + 1
        first.setdefault(sec, k)
    if sub in cnt:
        return sub
    if _ACC_SEC in cnt and len(cnt) > 1 and not _ACC_SUB.search(sub):
        cnt.pop(_ACC_SEC)
    return max(cnt, key=lambda sec: (cnt[sec], -first[sec]))


def is_iphone(sub):
    return sub.startswith("Apple iPhone")


def warranty_months(sub):
    return 12


def short_name(name):
    return re.sub(r"^(Телефон|Смартфон|Планшет|Ноутбук|Часы|Наушники)\s+", "", name)


def feed_items(d, idx):
    """Только новые товары в наличии, с ценой и фото."""
    for it in d["items"]:
        iid, sec, br, sub, name, price, stock, cond = it[:8]
        if cond != 0 or not stock or not price or iid not in idx:
            continue
        yield it


def yml(catalog_path, img_dir):
    data = _load(catalog_path, img_dir)
    if not data:
        return None
    d, idx, by_id, cached = data
    if cached:
        return cached
    e = html.escape
    secs, brands, subs = d["sections"], d["brands"], d["subs"]
    items = list(feed_items(d, idx))
    used_subs = sorted({it[3] for it in items})
    # родитель подраздела — как на сайте: раздел большинства всех товаров подраздела
    sub_secs = {}
    for it in d["items"]:
        sub_secs.setdefault(it[3], []).append(secs[it[1]])
    sec_idx = {n: k for k, n in enumerate(secs)}
    parent_of = {s: sec_idx[sub_section(subs[s], sub_secs[s])] for s in used_subs}
    used_secs = sorted({it[1] for it in items} | set(parent_of.values()))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<yml_catalog date="{time.strftime("%Y-%m-%dT%H:%M:%S+03:00")}">', "<shop>",
           f"<name>{SHOP}</name>", f"<company>{e(COMPANY)}</company>", f"<url>{BASE}/</url>",
           "<platform>ATOMM</platform>",
           '<currencies><currency id="RUR" rate="1"/></currencies>', "<categories>"]
    for s in used_secs:
        out.append(f'<category id="{s + 1}">{e(secs[s])}</category>')
    for s in used_subs:
        parent = parent_of[s] + 1
        out.append(f'<category id="{1000 + s}" parentId="{parent}">{e(subs[s])}</category>')
    out.append("</categories>")
    out.append(f'<delivery-options><option cost="{DELIVERY_COST}" days="0-1" order-before="15"/></delivery-options>')
    out.append('<pickup-options><option cost="0" days="0-1"/></pickup-options>')
    out.append("<offers>")
    for it in items:
        iid, sec, br, sub, name, price, stock, cond = it[:8]
        sub_name = subs[sub]
        vendor = brands[br] if br >= 0 else ""
        wm = warranty_months(sub_name)
        desc = (f"{name}. Новая оригинальная техника. Гарантия {wm} месяцев. "
                f"Доставка по Москве {DELIVERY_COST} ₽ или бесплатный самовывоз: {PICKUP}. Оплата при получении.")
        out.append(
            f'<offer id="{e(iid)}" available="true">'
            f"<url>{BASE}/p/{e(iid)}</url><price>{price}</price><currencyId>RUR</currencyId>"
            f"<categoryId>{1000 + sub}</categoryId><picture>{BASE}/img/{e(idx[iid])}</picture>"
            f"<name>{e(name)}</name>" + (f"<vendor>{e(vendor)}</vendor>" if vendor else "") +
            f"<description>{e(desc)}</description>"
            "<delivery>true</delivery><pickup>true</pickup><store>false</store>"
            "<manufacturer_warranty>true</manufacturer_warranty>"
            f'<param name="Гарантия">{wm} месяцев</param>'
            "</offer>")
    out.append("</offers></shop></yml_catalog>")
    xml = "\n".join(out)
    _cache["data"] = (d, idx, by_id, xml)
    return xml


def fmt_rub(n):
    return f"{n:,}".replace(",", " ") + " ₽"
