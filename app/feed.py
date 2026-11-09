"""Товарный YML-фид для Яндекса и страницы товаров /p/<id> (цена и фото видны роботу без JS)."""
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


def is_iphone(sub):
    return sub.startswith("Apple iPhone")


def warranty_months(sub):
    return 24 if is_iphone(sub) else 12


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
    used_secs = sorted({it[1] for it in items})
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<yml_catalog date="{time.strftime("%Y-%m-%dT%H:%M:%S+03:00")}">', "<shop>",
           f"<name>{SHOP}</name>", f"<company>{e(COMPANY)}</company>", f"<url>{BASE}/</url>",
           "<platform>ATOMM</platform>",
           '<currencies><currency id="RUR" rate="1"/></currencies>', "<categories>"]
    for s in used_secs:
        out.append(f'<category id="{s + 1}">{e(secs[s])}</category>')
    for s in used_subs:
        parent = next(it[1] for it in items if it[3] == s) + 1
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


PAGE = """<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — купить в Москве | ATOMM</title>
<meta name="description" content="{title} — {price_txt}. Новая оригинальная техника, гарантия {wm} месяцев. Доставка по Москве или бесплатный самовывоз.">
<link rel="canonical" href="{base}/p/{iid}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{title}"><meta property="og:image" content="{img}"><meta property="og:type" content="product">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script type="application/ld+json">{ld}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:radial-gradient(120% 70% at 50% 0%,#eef0f2 0%,#d9dbde 60%,#cbced2 100%) fixed;color:#1c1e21;font-family:Inter,system-ui,sans-serif;line-height:1.55;min-height:100vh}}
header{{padding:20px 32px;border-bottom:1px solid rgba(28,30,33,.13);display:flex;justify-content:space-between;align-items:center}}
.logo{{font-family:'JetBrains Mono',monospace;font-weight:500;letter-spacing:.34em;text-decoration:none;color:inherit}}
.logo i{{font-style:normal;color:#6b6f75;letter-spacing:.1em;margin-left:6px;font-weight:300}}
nav a{{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:inherit;opacity:.65;margin-left:22px;text-decoration:none}}
main{{max-width:1100px;margin:0 auto;padding:40px 32px 90px;display:grid;grid-template-columns:1.1fr 1fr;gap:40px;align-items:start}}
.ph{{aspect-ratio:1/1;border-radius:22px;background:radial-gradient(90% 90% at 50% 35%,#f6f7f8 0%,#dfe1e4 70%,#cfd2d6 100%);display:flex;align-items:center;justify-content:center;position:relative}}
.ph img{{width:74%;height:74%;object-fit:contain;mix-blend-mode:multiply}}
.ph .wr{{position:absolute;left:18px;top:14px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;font-weight:600}}
.crumb{{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#6b6f75}}
.crumb a{{color:inherit}}
h1{{font-weight:300;font-size:30px;letter-spacing:-.02em;line-height:1.2;margin:12px 0 18px}}
.price{{font-size:34px;font-weight:300;letter-spacing:-.02em;margin-bottom:22px}}
.btn{{display:inline-flex;justify-content:center;align-items:center;height:52px;padding:0 30px;border-radius:999px;background:#1c1e21;color:#fff;text-decoration:none;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase}}
dl{{display:grid;grid-template-columns:auto 1fr;gap:10px 22px;margin-top:28px;font-size:15px}}
dt{{color:#6b6f75}}
@media(max-width:860px){{main{{grid-template-columns:1fr;padding:24px 18px 60px;gap:22px}} header{{padding:16px 18px}} nav{{display:none}} h1{{font-size:24px}}}}
</style>
<script src="/analytics.js"></script>
</head><body>
<header><a class="logo" href="/">ATOMM<i>/store</i></a><nav><a href="/catalog.html">Каталог</a><a href="/delivery.html">Доставка</a><a href="/warranty.html">Гарантия</a><a href="/contacts.html">Контакты</a></nav></header>
<main>
<div class="ph">{wr_badge}<img src="{img}" alt="{title}"></div>
<div>
<div class="crumb"><a href="/catalog.html">Каталог</a> · {sec} · {sub}</div>
<h1>{name}</h1>
<div class="price">{price_txt}</div>
{buy}
<dl><dt>Состояние</dt><dd>Новый, оригинал</dd>
<dt>Наличие</dt><dd>{stock_txt}</dd>
<dt>Гарантия</dt><dd>{wm} месяцев · возврат и обмен 14 дней</dd>
<dt>Доставка</dt><dd>По Москве {dcost} ₽ — заказ до 15:00 привезём сегодня, с 17:00 до 22:00</dd>
<dt>Самовывоз</dt><dd>Бесплатно: {pickup}</dd>
<dt>Оплата</dt><dd>Наличными при получении</dd></dl>
</div>
</main>
<script src="/menu.js"></script>
</body></html>"""


def fmt_rub(n):
    return f"{n:,}".replace(",", " ") + " ₽"


def product_page(catalog_path, img_dir, iid):
    data = _load(catalog_path, img_dir)
    if not data:
        return None
    d, idx, by_id, _ = data
    it = by_id.get(iid)
    if not it:
        return None
    _, sec, br, sub, name, price, stock, cond = it[:8]
    sub_name = d["subs"][sub]
    e = html.escape
    wm = warranty_months(sub_name)
    img = f"{BASE}/img/{idx[iid]}" if iid in idx else f"{BASE}/apple-touch-icon.png"
    avail = bool(stock and price)
    ld = {"@context": "https://schema.org", "@type": "Product", "name": name, "image": img, "sku": iid,
          "brand": {"@type": "Brand", "name": d["brands"][br]} if br >= 0 else None,
          "offers": {"@type": "Offer", "url": f"{BASE}/p/{iid}", "priceCurrency": "RUB", "price": price,
                     "itemCondition": "https://schema.org/NewCondition",
                     "availability": "https://schema.org/InStock" if avail else "https://schema.org/OutOfStock"}}
    ld = {k: v for k, v in ld.items() if v is not None}
    buy = (f'<a class="btn" href="/catalog.html#item-{e(iid)}">Купить</a>' if avail
           else '<a class="btn" href="/catalog.html" style="background:#8a8e94">Нет в наличии — в каталог</a>')
    return PAGE.format(
        title=e(short_name(name)), name=e(name), base=BASE, iid=e(iid), img=e(img),
        ld=json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"),
        price_txt=fmt_rub(price) if price else "Цена по запросу", wm=wm,
        wr_badge='<span class="wr">2 года гарантии</span>' if is_iphone(sub_name) else "",
        sec=e(d["sections"][sec]), sub=e(sub_name), buy=buy,
        stock_txt="В наличии" if avail else "Нет в наличии", dcost=DELIVERY_COST, pickup=PICKUP)
