"""SEO-страницы ATOMM, которые сервер отдаёт готовым HTML (робот видит товары и цены без JS).

/catalog/                         — все разделы и модели
/catalog/<раздел>/                — раздел (smartphones, tablets, ...)
/catalog/<подборка>/              — подборки: iphone, ipad, mac, apple-watch, airpods, samsung-galaxy, ...
/catalog/<модель>/                — модель, напр. /catalog/apple-iphone-18-pro-max/
/catalog/<модель>/<память>/       — модель + объём памяти, напр. /catalog/apple-iphone-18-pro-max/256gb/
/p/<id>                           — товар
/guides/<slug>/                   — статьи-гайды (seo_content.GUIDES)
/sitemap.xml                      — карта сайта из актуального каталога
"""
import html
import json
import os
import re
import time
from urllib.parse import quote

import feed
import seo_content

BASE = feed.BASE
PICKUP = feed.PICKUP
DELIVERY_COST = feed.DELIVERY_COST
PHONE = "+79777773727"
PHONE_TXT = "+7 977 777-37-27"
MEM_PAGES_FOR = ("Apple iPhone", "Apple iPad", "Samsung Galaxy S", "Samsung Galaxy Z")
LIST_LIMIT = 96          # сколько товаров выводим на странице раздела/модели
e = html.escape

SECTION_SLUGS = {
    "Смартфоны": "smartphones", "Планшеты": "tablets", "Ноутбуки и компьютеры": "laptops",
    "Часы и браслеты": "watches", "Аудио": "audio", "Игры и приставки": "gaming",
    "Техника для дома и красоты": "home", "Камеры и дроны": "cameras", "Аксессуары": "accessories",
}

# как раздел звучит в «Купить …» / «цена на …»
SECTION_ACC = {
    "Смартфоны": "смартфоны", "Планшеты": "планшеты", "Ноутбуки и компьютеры": "ноутбуки и компьютеры",
    "Часы и браслеты": "умные часы и фитнес-браслеты", "Аудио": "наушники и колонки",
    "Игры и приставки": "игровые приставки", "Техника для дома и красоты": "технику для дома и красоты",
    "Камеры и дроны": "экшн-камеры и дроны", "Аксессуары": "аксессуары",
}

# подборки «бренд/линейка» — под частые запросы «купить айфон», «купить макбук» и т. п.
COLLECTIONS = [
    # slug, H1, родительный/винительный для текста, раздел (или None), фильтр по имени подраздела
    ("iphone", "Apple iPhone", "iPhone (айфон)", "Смартфоны", lambda s, b: s.startswith("Apple iPhone")),
    ("ipad", "Apple iPad", "iPad (айпад)", "Планшеты", lambda s, b: "iPad" in s),
    ("mac", "Apple MacBook и Mac", "MacBook и Mac (макбук)", "Ноутбуки и компьютеры", lambda s, b: b == "Apple"),
    ("apple-watch", "Apple Watch", "Apple Watch (эпл вотч)", "Часы и браслеты", lambda s, b: "Apple Watch" in s),
    ("airpods", "AirPods", "AirPods (аирподс)", "Аудио", lambda s, b: "AirPods" in s or s == "Наушники Apple"),
    ("samsung-galaxy", "Смартфоны Samsung Galaxy", "Samsung Galaxy (самсунг)", "Смартфоны", lambda s, b: b == "Samsung"),
    ("xiaomi", "Смартфоны Xiaomi, Redmi и Poco", "Xiaomi, Redmi и Poco (сяоми)", "Смартфоны", lambda s, b: b == "Xiaomi"),
    ("huawei", "Смартфоны Huawei", "Huawei (хуавей)", "Смартфоны", lambda s, b: b == "Huawei"),
    ("dyson", "Техника Dyson", "Dyson (дайсон)", None, lambda s, b: b == "Dyson"),
    ("playstation", "Sony PlayStation", "PlayStation (плейстейшен)", "Игры и приставки", lambda s, b: "Playstation" in s or "PlayStation" in s),
]

_TR = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
               ["a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s",
                "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya"]))

# русские написания моделей — так их часто ищут в Яндексе
_RU = [(r"\biPhone\b", "айфон"), (r"\bPro Max\b", "про макс"), (r"\bPro\b", "про"), (r"\bMax\b", "макс"),
       (r"\bAir\b", "эйр"), (r"\bPlus\b", "плюс"), (r"\bmini\b", "мини"), (r"\bUltra\b", "ультра"),
       (r"\biPad\b", "айпад"), (r"\bMacBook\b", "макбук"), (r"\bGalaxy\b", "галакси"), (r"\bWatch\b", "вотч"),
       (r"\bAirPods\b", "аирподс"), (r"\bSamsung\b", "самсунг"), (r"\bXiaomi\b", "сяоми")]


def sub_section(sub, its):
    """Раздел подраздела — по большинству товаров (общая логика с фидом, см. feed.sub_section)."""
    return feed.sub_section(sub, [it["sec"] for it in its])


def slugify(s):
    s = s.lower().replace("+", " plus ").replace('"', " ")
    s = "".join(_TR.get(ch, ch) for ch in s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def ru_name(sub):
    """'Apple iPhone 18 Pro Max' -> 'айфон 18 про макс' (или '' если переводить нечего)."""
    s = re.sub(r"^Apple\s+", "", sub)
    r = s
    for a, b in _RU:
        r = re.sub(a, b, r)
    return r if r != s and not re.search(r"[A-Za-z]", r) else ""


def ru_title(ru):
    """'айфон 18 про макс' -> 'айфон 18 Про Макс' (для title: бренд строчными, как в запросах, линейка с заглавной)."""
    return " ".join(w if w == "айфон" or not w[:1].isalpha() else w[:1].upper() + w[1:] for w in ru.split())


def plain(sub):
    """Название модели без бренда Apple для заголовков: 'Apple iPhone 17' -> 'iPhone 17'."""
    return re.sub(r"^Apple\s+(?=iPhone|iPad|MacBook|Macbook|AirPods|Mac|iMac|HomePod)", "", sub)


def is_generic(sub):
    """Не модель, а группа товаров («Портативная акустика», «Телефоны Samsung», «Для планшетов»)."""
    return bool(re.match(r"[А-ЯЁа-яё]", sub))


def display(sub, sec):
    """Название подраздела для H1/заголовков."""
    if sub.startswith("Для "):
        return f"{sec} {sub[:1].lower()}{sub[1:]}"
    return plain(sub)


def crumb_label(sub, sec):
    """Подпись подраздела в крошках: тёзка раздела («Аксессуары» в «Аксессуарах») — «Все аксессуары»."""
    return f"Все {sec[:1].lower()}{sec[1:]}" if sub == sec else display(sub, sec)


def lower_first(s):
    return s[:1].lower() + s[1:] if s[:1].isalpha() and not s[:2].isupper() and re.match(r"[А-Я][а-я]", s) else s


def months(n):
    return f"{n} {plural(n, ['месяц', 'месяца', 'месяцев'])}"


def plural(n, f):
    a, b = n % 100, n % 10
    if 10 < a < 20:
        return f[2]
    if b == 1:
        return f[0]
    if 2 <= b <= 4:
        return f[1]
    return f[2]


rub = feed.fmt_rub
_MEM = re.compile(r"(\d+)\s*(ГБ|ТБ|GB|TB)\b", re.I)
_COLOR = re.compile(r"цвет:\s*([^,()]+?)\s*(?:\(|,|$)", re.I)


def memory_of(name, section):
    """Объём накопителя: для смартфонов/планшетов — последний «N ГБ/ТБ» в названии."""
    if section not in ("Смартфоны", "Планшеты"):
        return None
    m = _MEM.findall(name)
    if not m:
        return None
    n, u = m[-1]
    u = u.upper().replace("GB", "ГБ").replace("TB", "ТБ")
    gb = int(n) * (1024 if u == "ТБ" else 1)
    return gb


def mem_label(gb):
    return f"{gb // 1024} ТБ" if gb >= 1024 and gb % 1024 == 0 else f"{gb} ГБ"


def mem_slug(gb):
    return f"{gb // 1024}tb" if gb >= 1024 and gb % 1024 == 0 else f"{gb}gb"


_COLOR_FULL = re.compile(r"цвет:\s*([^,]+)", re.I)
_SIM_BOTH = "Можно выбрать версию только с eSIM или с Nano SIM + eSIM — тип SIM указан в названии каждого товара."
_SIM_ESIM = "Все варианты в наличии — только с eSIM, без лотка для физической SIM-карты."
_SIM_NANO = "Все варианты в наличии — с Nano SIM + eSIM: можно вставить обычную SIM-карту."
_FMT = __import__("string").Formatter()


def sim_kind(name):
    if re.search(r"nano", name, re.I):
        return "nano"
    if re.search(r"esim", name, re.I):
        return "esim"
    return None


def join_ru(xs):
    xs = list(xs)
    return ", ".join(xs[:-1]) + " и " + xs[-1] if len(xs) > 1 else (xs[0] if xs else "")


def color_of(name):
    m = _COLOR.search(name)
    return m.group(1).strip().lower() if m else None


# ---------------------------------------------------------------- модель данных
_cache = {"key": None, "m": None}


def model(catalog_path, img_dir):
    data = feed._load(catalog_path, img_dir)
    if not data:
        return None
    key = feed._cache["key"]
    if _cache["key"] == key and _cache["m"]:
        return _cache["m"]
    d, idx, by_id, _ = data
    secs, brands, subs = d["sections"], d["brands"], d["subs"]
    items = []
    for pos, it in enumerate(d["items"]):
        iid, sec, br, sub, name, price, stock, cond = it[:8]
        items.append({"id": iid, "sec": secs[sec], "brand": brands[br] if br >= 0 else "", "sub": subs[sub],
                      "name": name, "price": price, "stock": bool(stock and price), "cond": cond,
                      "img": idx.get(iid), "pos": pos, "mem": memory_of(name, secs[sec]), "color": color_of(name)})
    sub_items = {}
    for it in items:
        sub_items.setdefault(it["sub"], []).append(it)
    sub_sec = {s: sub_section(s, its) for s, its in sub_items.items()}
    # слаги моделей; при совпадении — добавляем раздел
    used = set(SECTION_SLUGS.values()) | {c[0] for c in COLLECTIONS}
    sub_slug = {}
    for s in subs:
        if s not in sub_items:
            continue
        sl = slugify(s)
        if sl in used:
            sl = f"{sl}-{SECTION_SLUGS.get(sub_sec[s], 'x')}"
        while sl in used:
            sl += "-2"
        used.add(sl)
        sub_slug[s] = sl
    pages = {}
    for sec_name, sl in SECTION_SLUGS.items():
        its = [it for it in items if it["sec"] == sec_name]
        if its:
            pages[sl] = {"kind": "section", "slug": sl, "title": sec_name, "sec": sec_name, "items": its}
    for sl, h1, ru, sec_name, f in COLLECTIONS:
        its = [it for it in items if (sec_name is None or it["sec"] == sec_name) and f(it["sub"], it["brand"])]
        if its:
            pages[sl] = {"kind": "collection", "slug": sl, "title": h1, "ru": ru, "sec": sec_name, "items": its}
    coll_sets = {sl: {it["id"] for it in p["items"]} for sl, p in pages.items() if p["kind"] == "collection"}
    for s in list(sub_slug):
        ids = {it["id"] for it in sub_items[s]}
        same = next((sl for sl, cs in coll_sets.items() if cs == ids), None)
        if same:                      # модель = подборка (PlayStation) — одна страница вместо двух
            sub_slug[s] = same
    for s, sl in sub_slug.items():
        if sl in pages:
            continue
        its = sub_items[s]
        p = {"kind": "model", "slug": sl, "title": s, "sec": sub_sec[s], "sub": s, "items": its, "mems": {}}
        # страницы «модель + память» — только для линеек, которые так ищут (iphone 18 pro max 256)
        cnt = {}
        for it in its:
            if it["mem"] and it["stock"]:
                cnt[it["mem"]] = cnt.get(it["mem"], 0) + 1
        mems = sorted(gb for gb, n in cnt.items() if n >= 2)
        if len(mems) >= 2 and s.startswith(MEM_PAGES_FOR):
            for gb in mems:
                p["mems"][mem_slug(gb)] = gb
        pages[sl] = p
    m = {"items": items, "by_id": {it["id"]: it for it in items}, "subs": [s for s in subs if s in sub_slug],
         "sub_slug": sub_slug, "sub_items": sub_items, "sub_sec": sub_sec, "pages": pages,
         "secs": [s for s in secs if s in SECTION_SLUGS and SECTION_SLUGS[s] in pages],
         "date": time.strftime("%Y-%m-%d", time.localtime(max(os.path.getmtime(catalog_path), 0)))}
    _cache.update(key=key, m=m)
    return m


def in_stock(its):
    return [it for it in its if it["stock"]]


def price_range(its):
    p = [it["price"] for it in its if it["stock"] and it["price"]]
    return (min(p), max(p)) if p else (None, None)


def sec_url(sec):
    return f"/catalog/{SECTION_SLUGS[sec]}/"


def sub_url(m, sub):
    return f"/catalog/{m['sub_slug'][sub]}/"


def short(it):
    return feed.short_name(it["name"])


# ---------------------------------------------------------------- общая вёрстка
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:radial-gradient(120% 70% at 50% 0%,#eef0f2 0%,#d9dbde 60%,#cbced2 100%) fixed;color:#1c1e21;font-family:Inter,system-ui,sans-serif;line-height:1.55;min-height:100vh;-webkit-font-smoothing:antialiased}
a{color:inherit}
.mono{font-family:'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;font-size:11px}
header{padding:20px 32px;border-bottom:1px solid rgba(28,30,33,.13);display:flex;justify-content:space-between;align-items:center;gap:20px}
.logo{font-family:'JetBrains Mono',monospace;font-weight:500;letter-spacing:.34em;text-decoration:none;color:inherit;white-space:nowrap}
.logo i{font-style:normal;color:#6b6f75;letter-spacing:.1em;margin-left:6px;font-weight:300}
header nav a{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:inherit;opacity:.65;margin-left:22px;text-decoration:none}
header nav a:hover{opacity:1}
.page{max-width:1240px;margin:0 auto;padding:28px 32px 70px}
.crumb{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#6b6f75}
.crumb a{color:inherit;text-decoration:none}.crumb a:hover{text-decoration:underline}
h1{font-weight:200;font-size:clamp(30px,4vw,52px);letter-spacing:-.035em;line-height:1.05;margin:14px 0 12px}
h2{font-weight:300;font-size:clamp(22px,2.4vw,30px);letter-spacing:-.02em;line-height:1.15;margin:44px 0 16px}
h3{font-weight:500;font-size:16px;margin:0 0 6px}
.lead{max-width:860px;color:#3f4348;font-size:16px}
.lead p+p{margin-top:10px}
.facts{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0 6px}
.facts span{border:1px solid rgba(28,30,33,.14);border-radius:999px;padding:7px 14px;font-size:13px;background:rgba(245,246,247,.45)}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 4px}
.chips a{border:1px solid rgba(28,30,33,.16);border-radius:999px;padding:7px 14px;font-size:13px;text-decoration:none;background:rgba(245,246,247,.4)}
.chips a.on,.chips a:hover{background:#1c1e21;color:#eef0f2;border-color:#1c1e21}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px;margin-top:22px}
.card{background:rgba(233,234,236,.7);border:1px solid rgba(28,30,33,.08);border-radius:18px;padding:14px;display:flex;flex-direction:column;text-decoration:none}
.card:hover{border-color:rgba(28,30,33,.25)}
.card .ph{aspect-ratio:1/1;border-radius:12px;background:radial-gradient(90% 90% at 50% 35%,#f6f7f8 0%,#dfe1e4 70%,#cfd2d6 100%);display:flex;align-items:center;justify-content:center;margin-bottom:12px}
.card .ph img{width:78%;height:78%;object-fit:contain;mix-blend-mode:multiply}
.card .nm{font-size:14px;line-height:1.35;flex:1}
.card .pr{font-size:18px;font-weight:400;margin-top:10px}
.card .st{font-size:12px;color:#6b6f75;margin-top:2px}
.card .st.no{color:#a8323a}
.more{margin-top:20px;font-size:14px}
.btn{display:inline-flex;justify-content:center;align-items:center;height:48px;padding:0 26px;border-radius:999px;background:#1c1e21;color:#fff;text-decoration:none;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase}
.models{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px;margin-top:14px}
.models a{display:flex;justify-content:space-between;gap:10px;padding:12px 14px;border-radius:12px;border:1px solid rgba(28,30,33,.1);text-decoration:none;background:rgba(245,246,247,.35);font-size:14px}
.models a:hover{border-color:rgba(28,30,33,.3)}
.models a small{color:#6b6f75;white-space:nowrap}
.faq{max-width:860px}
.faq details{border-top:1px solid rgba(28,30,33,.12);padding:14px 0}
.faq summary{cursor:pointer;font-size:16px;font-weight:400}
.faq details p{margin-top:8px;color:#3f4348}
.seclist h3{margin-top:26px}
footer{border-top:1px solid rgba(28,30,33,.13);padding:34px 32px 50px;font-size:13px;color:#4a4e54}
footer .in{max-width:1240px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px}
footer a{text-decoration:none;display:block;padding:2px 0}footer a:hover{text-decoration:underline}
footer .mono{color:#6b6f75;margin-bottom:8px}
.pmain{display:grid;grid-template-columns:1.1fr 1fr;gap:40px;align-items:start;margin-top:18px}
.pmain .big{aspect-ratio:1/1;border-radius:22px;background:radial-gradient(90% 90% at 50% 35%,#f6f7f8 0%,#dfe1e4 70%,#cfd2d6 100%);display:flex;align-items:center;justify-content:center;position:relative}
.pmain .big img{width:74%;height:74%;object-fit:contain;mix-blend-mode:multiply}
.pmain .wr{position:absolute;left:18px;top:14px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;font-weight:600}
.pmain h1{font-size:clamp(24px,2.6vw,32px);font-weight:300;letter-spacing:-.02em;line-height:1.2;margin:12px 0 18px}
.price{font-size:34px;font-weight:300;letter-spacing:-.02em;margin-bottom:22px}
dl{display:grid;grid-template-columns:auto 1fr;gap:10px 22px;margin-top:28px;font-size:15px}
dt{color:#6b6f75}
.seo-text a,.article a{text-decoration:underline}
.article{max-width:860px;color:#3f4348;font-size:16px}.article p{margin-top:10px}.article h2{color:#1c1e21}
.article .meta{font-size:13px;color:#6b6f75;margin-top:6px}.article .src{font-size:13px;color:#6b6f75;margin-top:28px}
.cmp{width:100%;border-collapse:collapse;margin:14px 0;font-size:14px}.cmp th,.cmp td{text-align:left;padding:9px 10px;border-bottom:1px solid rgba(28,30,33,.12);vertical-align:top}
.cmp th{font-weight:500}
@media(max-width:860px){.cmp{font-size:13px}.cmp th,.cmp td{padding:7px 5px}}
@media(max-width:860px){header{padding:16px 18px}header nav{display:none}.page{padding:20px 18px 50px}.pmain{grid-template-columns:1fr;gap:22px}.grid{grid-template-columns:repeat(2,1fr);gap:10px}.card{padding:10px}.card .pr{font-size:16px}footer{padding:28px 18px 40px}}
"""


def _ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def breadcrumbs(trail):
    """trail: [(name, url|None)] — HTML + JSON-LD BreadcrumbList."""
    full = [("Главная", "/"), ("Каталог", "/catalog/")] + trail
    parts = []
    for k, (n, u) in enumerate(full):
        parts.append(f'<a href="{e(u)}">{e(n)}</a>' if u and k < len(full) - 1 else f"<span>{e(n)}</span>")
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": n, **({"item": BASE + u} if u else {})}
        for k, (n, u) in enumerate(full)]}
    return '<nav class="crumb" aria-label="Навигация">' + " · ".join(parts) + "</nav>", _ld(ld)


def footer(m):
    cols = []
    if m:
        top = [("iphone", "iPhone"), ("ipad", "iPad"), ("mac", "MacBook и Mac"), ("apple-watch", "Apple Watch"),
               ("airpods", "AirPods"), ("samsung-galaxy", "Samsung Galaxy"), ("dyson", "Dyson"),
               ("playstation", "PlayStation")]
        cols.append('<div><div class="mono">Популярное</div>' + "".join(
            f'<a href="/catalog/{s}/">{e(t)}</a>' for s, t in top if s in m["pages"]) + "</div>")
        models = [s for s in m["subs"] if s.startswith("Apple iPhone")][:8]
        cols.append('<div><div class="mono">iPhone</div>' + "".join(
            f'<a href="{sub_url(m, s)}">{e(plain(s))}</a>' for s in models) + "</div>")
        cols.append('<div><div class="mono">Разделы</div>' + "".join(
            f'<a href="{sec_url(s)}">{e(s)}</a>' for s in m["secs"]) + "</div>")
    cols.append(f'<div><div class="mono">ATOMM</div><a href="tel:{PHONE}">{PHONE_TXT}</a>'
                f'<a href="/delivery.html">Доставка по Москве</a><a href="/warranty.html">Гарантия и возврат</a>'
                f'<a href="/contacts.html">Контакты</a><span style="display:block;margin-top:8px">Самовывоз: {e(PICKUP)}</span></div>')
    return '<footer><div class="in">' + "".join(cols) + "</div></footer>"


def layout(title, desc, canonical, body, m, ld_blocks="", robots=None, og_image=None):
    canon = f'<link rel="canonical" href="{BASE}{e(canonical)}">' if canonical else ""
    og = f'<meta property="og:image" content="{e(og_image)}">' if og_image else ""
    rb = f'<meta name="robots" content="{robots}">' if robots else ""
    return f"""<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{canon}{rb}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{BASE}{e(canonical or '/')}"><meta property="og:type" content="website"><meta property="og:site_name" content="ATOMM">{og}
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta name="theme-color" content="#d7d9dc">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
{ld_blocks}
<script src="/analytics.js"></script>
</head><body>
<header><a class="logo" href="/">ATOMM<i>/store</i></a><nav><a href="/catalog/">Каталог</a><a href="/catalog/iphone/">iPhone</a><a href="/delivery.html">Доставка</a><a href="/warranty.html">Гарантия</a><a href="/contacts.html">Контакты</a></nav></header>
<main class="page">
{body}
</main>
{footer(m)}
<script src="/menu.js"></script>
</body></html>"""


def card(it):
    img = (f'<img src="/img/{e(it["img"])}" alt="{e(short(it))}" loading="lazy" width="300" height="300">'
           if it["img"] else "")
    st = ('<div class="st">В наличии</div>' if it["stock"] else '<div class="st no">Нет в наличии</div>')
    pr = rub(it["price"]) if it["price"] else "Цена по запросу"
    return (f'<a class="card" href="/p/{e(it["id"])}"><div class="ph">{img}</div>'
            f'<div class="nm">{e(short(it))}</div><div class="pr">{pr}</div>{st}</a>')


def grid(its, more_url=None):
    its = sorted(its, key=lambda it: (not it["stock"], it["pos"]))
    h = '<div class="grid">' + "".join(card(it) for it in its[:LIST_LIMIT]) + "</div>"
    if len(its) > LIST_LIMIT and more_url:
        h += f'<p class="more">Показаны {LIST_LIMIT} из {len(its)}. <a href="{e(more_url)}">Все товары и фильтры — в каталоге</a></p>'
    return h


def faq_block(qa):
    """qa: [(вопрос, ответ)] или [(вопрос, ответ-текст, ответ-HTML)] — HTML показывается на странице, текст — в JSON-LD."""
    qa = [x for x in qa if x[1].strip()]
    h = '<section class="faq"><h2>Вопросы и ответы</h2>' + "".join(
        f"<details><summary>{e(x[0])}</summary><p>{x[2] if len(x) > 2 else e(x[1])}</p></details>" for x in qa) + "</section>"
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": x[0], "acceptedAnswer": {"@type": "Answer", "text": x[1]}} for x in qa]}
    return h, _ld(ld)


def agg_offer_ld(name, url, its, img=None, brand=None):
    lo, hi = price_range(its)
    if lo is None:
        return ""
    ld = {"@context": "https://schema.org", "@type": "Product", "name": name, "url": BASE + url,
          "offers": {"@type": "AggregateOffer", "priceCurrency": "RUB", "lowPrice": lo, "highPrice": hi,
                     "offerCount": len(in_stock(its)), "availability": "https://schema.org/InStock",
                     "itemCondition": "https://schema.org/NewCondition"}}
    if img:
        ld["image"] = f"{BASE}/img/{img}"
    if brand:
        ld["brand"] = {"@type": "Brand", "name": brand}
    return _ld(ld)


def common_faq(name, its, wm):
    by = "объёма памяти и цвета" if any(it["mem"] for it in its) else "модели и комплектации"
    lo, hi = price_range(its)
    n = len(in_stock(its))
    qa = []
    if lo:
        qa.append((f"Какая цена на {name} в Москве?",
                   f"В ATOMM цены на {name} — от {rub(lo)} до {rub(hi)} в зависимости от {by}. "
                   f"Сейчас в наличии {n} {plural(n, ['вариант', 'варианта', 'вариантов'])}, цены обновляются несколько раз в день."))
    qa += [
        ("Это оригинальная новая техника?",
         "Да. Мы продаём только новые оригинальные устройства в заводской упаковке. Перед отправкой проверяем каждый товар."),
        ("Как быстро доставите по Москве?",
         f"Если оформить заказ до 15:00, привезём в тот же день с 17:00 до 22:00. Доставка по Москве — {DELIVERY_COST} ₽. "
         f"Бесплатный самовывоз: {PICKUP}."),
        ("Как оплатить заказ?", "Наличными при получении — курьеру или на самовывозе. Предоплата не нужна."),
        ("Какая гарантия?",
         f"Гарантия магазина — {months(wm)}. Возврат и обмен — в течение 14 дней по закону о защите прав потребителей."),
    ]
    return qa


def facts_html(wm):
    return ('<div class="facts">'
            f"<span>Новые, оригинал</span><span>Гарантия {wm} мес.</span>"
            f"<span>Доставка сегодня при заказе до 15:00</span><span>Самовывоз бесплатно</span>"
            "<span>Оплата при получении</span></div>")


# ---------------------------------------------------------------- страницы
def page_hub(m):
    crumbs, crumbs_ld = breadcrumbs([])
    crumbs = crumbs.replace('<a href="/catalog/">Каталог</a>', "<span>Каталог</span>")
    body = [crumbs, "<h1>Каталог техники</h1>",
            '<div class="lead"><p>Новая оригинальная техника с доставкой по Москве: iPhone, iPad, MacBook, Apple Watch, '
            'AirPods, Samsung Galaxy, Xiaomi, Dyson, PlayStation и другое. Цены обновляются несколько раз в день. '
            '<a href="/catalog.html">Открыть каталог с фильтрами и корзиной</a>.</p></div>',
            facts_html(12), '<div class="chips">' + "".join(
                f'<a href="/catalog/{c[0]}/">{e(c[1])}</a>' for c in COLLECTIONS if c[0] in m["pages"]) + "</div>",
            '<div class="seclist">']
    for sec in m["secs"]:
        subs = [s for s in m["subs"] if m["sub_sec"][s] == sec]
        body.append(f'<h2><a href="{sec_url(sec)}" style="text-decoration:none">{e(sec)}</a></h2>{models_list(m, subs)}')
    body.append("</div>")
    return layout("Каталог техники Apple, Samsung, Xiaomi, Dyson — купить в Москве | ATOMM",
                  "Каталог ATOMM: iPhone, iPad, MacBook, Apple Watch, AirPods, Samsung, Xiaomi, Dyson, PlayStation. "
                  "Новая оригинальная техника, доставка по Москве в день заказа, оплата при получении.",
                  "/catalog/", "\n".join(body), m, crumbs_ld)


def models_list(m, subs):
    rows = []
    for s in subs:
        its = m["sub_items"][s]
        lo, _ = price_range(its)
        n = len(in_stock(its))
        info = f"от {rub(lo)}" if lo else "нет в наличии"
        rows.append(f'<a href="{sub_url(m, s)}"><span>{e(display(s, m["sub_sec"][s]))}</span><small>{info}</small></a>')
    return '<div class="models">' + "".join(rows) + "</div>"


def page_group(m, p):
    """Раздел или подборка."""
    its = p["items"]
    name = p["title"]
    trail = [(name, None)]
    if p["kind"] == "collection" and p["sec"]:
        trail = [(p["sec"], sec_url(p["sec"])), (name, None)]
    crumbs, crumbs_ld = breadcrumbs(trail)
    subs = []
    for it in its:
        if it["sub"] not in subs:
            subs.append(it["sub"])
    subs.sort(key=lambda s: m["subs"].index(s))
    lo, hi = price_range(its)
    n = len(in_stock(its))
    wm = 24 if p["slug"] == "iphone" else 12
    ru = p.get("ru") or SECTION_ACC.get(name) or lower_first(name)
    acc = ({"dyson": "технику Dyson"}.get(p["slug"]) or lower_first(name)) if p["kind"] == "collection" \
        else SECTION_ACC.get(name, lower_first(name))
    intro = (f"<p>В ATOMM в наличии {n} {plural(n, ['товар', 'товара', 'товаров'])} в разделе «{e(name)}»"
             + (f" — цены от {rub(lo)}" if lo else "") + ". "
             f"Только новые оригинальные устройства, доставка по Москве в день заказа и бесплатный самовывоз.</p>"
             f"<p>Выберите модель ниже, чтобы увидеть все варианты по памяти и цвету.</p>")
    body = [crumbs, f"<h1>{e(name)}</h1>", f'<div class="lead">{intro}</div>', facts_html(wm)]
    if len(subs) > 1:
        body.append(f"<h2>Модели</h2>{models_list(m, subs)}")
    body.append(f"<h2>Товары</h2>{grid(its, '/catalog.html')}")
    qa = common_faq(ru, its, wm)
    fh, fld = faq_block(qa)
    body.append(fh)
    title = f"Купить {acc} в Москве" + (
        f" — цены от {rub(lo)}" if lo else "") + " | ATOMM"
    desc = (f"{name} в ATOMM: {n} {plural(n, ['товар', 'товара', 'товаров'])} в наличии" + (f", от {rub(lo)}" if lo else "")
            + ". Новая оригинальная техника, доставка по Москве сегодня при заказе до 15:00, оплата при получении.")
    url = f"/catalog/{p['slug']}/"
    return layout(title, desc, url, "\n".join(body), m,
                  crumbs_ld + fld)


def variants_ctx(p):
    """Данные каталога для текстов seo_content — только по товарам в наличии. Нет наличия/данных — пустые строки
    (фрагменты текста с пустыми плейсхолдерами не выводятся)."""
    its = in_stock(p["items"])
    colors = []
    for it in its:
        mt = _COLOR_FULL.search(it["name"])
        c = mt.group(1).strip() if mt else None
        if c and c not in colors:
            colors.append(c)
    mems = sorted({it["mem"] for it in its if it["mem"]})
    sims = {sim_kind(it["name"]) for it in its} - {None}
    sim = _SIM_BOTH if {"nano", "esim"} <= sims else _SIM_ESIM if sims == {"esim"} else _SIM_NANO if sims == {"nano"} else ""
    lo, _ = price_range(p["items"])
    links = ", ".join(f'<a href="/catalog/{p["slug"]}/{ms}/">{mem_label(gb)}</a>' for ms, gb in p["mems"].items())
    sim_answer = ("Да, есть: в наличии версии с Nano SIM + eSIM и только с eSIM — тип SIM указан в названии каждого товара."
                  if {"nano", "esim"} <= sims else
                  "Да, все варианты в наличии — с Nano SIM + eSIM: можно вставить обычную SIM-карту." if sims == {"nano"} else
                  "Нет, в наличии только версии с eSIM — без лотка для физической SIM-карты." if sims == {"esim"} else "")
    return {"colors": join_ru(colors), "mems": join_ru(mem_label(x) for x in mems), "sim": sim, "sim_answer": sim_answer,
            "lo": f"от {rub(lo)}" if lo else "", "mem_links": (links, "")}


def text_ctx(m, p):
    """Плейсхолдеры: значения — строка (экранируется) или пара (html, text) для доверенного HTML."""
    ctx = variants_ctx(p)
    for sl, pg in m["pages"].items():
        if pg["kind"] == "model" and in_stock(pg["items"]):
            nm = display(pg["sub"], pg["sec"])
            ctx["link_" + sl.replace("-", "_")] = (f'<a href="/catalog/{sl}/">{e(nm)}</a>', nm)
    gt = seo_content.GUIDES["iphone-18-pro-vs-18-pro-max"]["title"]
    ctx["guide"] = (f'<a href="{seo_content.GUIDE_18PRO}">«{e(gt)}»</a>', f"«{gt}»")
    return ctx


def _frag(t, ctx, as_html):
    """Фрагмент текста или None, если какой-то плейсхолдер пуст/неизвестен."""
    vals = {}
    for _, k, _, _ in _FMT.parse(t):
        if k is None:
            continue
        v = ctx.get(k)
        if isinstance(v, tuple):
            v = v[0] if as_html else v[1]
        elif v and as_html:
            v = e(v)
        if not v:
            return None
        vals[k] = v
    return t.format_map(vals)


def frags(parts, ctx, as_html):
    out = [_frag(t, ctx, as_html) for t in parts]
    return out[0] is not None, " ".join(x for x in out if x)


def model_text(m, p):
    """(HTML-блок с H2, доп. вопросы FAQ [(q, text, html)]) для страницы модели из seo_content.MODELS или ("", [])."""
    c = seo_content.MODELS.get(p["slug"])
    if not c:
        return "", []
    ctx = text_ctx(m, p)
    paras = "".join(f"<p>{h}</p>" for h in (frags(t, ctx, True)[1] for t in c["paras"]) if h)
    qa = []
    for q, parts in c.get("faq", []):
        ok, txt = frags(parts, ctx, False)
        if ok and txt.strip():
            qa.append((q, re.sub(r"\s+", " ", txt).strip(), frags(parts, ctx, True)[1]))
    return (f'<h2>{e(c["h2"])}</h2><div class="lead seo-text">{paras}</div>' if paras else ""), qa


def model_title(full, sub, ru, lo, mem=False):
    """Title модели. Русская форма — только для iPhone (ru_name «айфон …») без скобок/кавычек в названии;
    длину держим ≤ 80 символов, слово «цена» стараемся сохранить."""
    plain_t = f"Купить {full} в Москве" + (f" — цена от {rub(lo)}" if lo else "") + " | ATOMM"
    if not (ru.startswith("айфон") and "(" not in sub and '"' not in sub):
        return plain_t
    rt = ru_title(ru)
    if lo:
        cands = [f"Купить {full} ({rt}) в Москве — цена от {rub(lo)} | ATOMM",
                 f"{full} ({rt}) — купить в Москве, цена от {rub(lo)} | ATOMM",
                 f"{full} ({rt}) — цена в Москве от {rub(lo)} | ATOMM"]
    else:
        cands = [f"Купить {full} ({rt}) в Москве | ATOMM"]
    if mem:          # страницы памяти: единый вид «Купить …», без альтернативных формулировок
        cands = cands[:1]
    return next((t for t in cands if len(t) <= 80), plain_t)


def page_model(m, p, mem=None):
    sub = p["sub"]
    its = p["items"]
    if mem:
        its = [it for it in its if it["mem"] == mem]
    nm = display(sub, p["sec"])
    gen = is_generic(sub)
    ru = ru_name(sub)
    full = nm + (f" {mem_label(mem)}" if mem else "")
    url = f"/catalog/{p['slug']}/" + (f"{mem_slug(mem)}/" if mem else "")
    trail = [(p["sec"], sec_url(p["sec"]))]
    if sub.startswith("Apple iPhone"):
        trail.append(("iPhone", "/catalog/iphone/"))
    trail.append((crumb_label(sub, p["sec"]), f"/catalog/{p['slug']}/" if mem else None))
    if mem:
        trail.append((mem_label(mem), None))
    crumbs, crumbs_ld = breadcrumbs(trail)
    lo, hi = price_range(its)
    st = in_stock(its)
    n = len(st)
    wm = feed.warranty_months(sub)
    mems = sorted({it["mem"] for it in st if it["mem"]})
    colors = []
    for it in st:
        if it["color"] and it["color"] not in colors:
            colors.append(it["color"])
    brand = next((it["brand"] for it in its if it["brand"]), "")
    alt = f" ({ru}{' ' + mem_label(mem).lower() if mem else ''})" if ru else ""
    head = f"{e(full)} в ATOMM: " if gen else f"Купить {e(full)}{e(alt)} в Москве можно в ATOMM: "
    p1 = (head
          + (f"в наличии {n} {plural(n, ['вариант', 'варианта', 'вариантов'])} по цене от {rub(lo)}"
             + (f" до {rub(hi)}" if hi and hi != lo else "") if n else "сейчас нет в наличии — оставьте заявку по телефону, привезём под заказ")
          + ".")
    det = []
    if mems and not mem:
        det.append("объём памяти: " + ", ".join(mem_label(x) for x in mems))
    if colors:
        det.append("цвета: " + ", ".join(colors[:12]))
    has_text = not mem and p["slug"] in seo_content.MODELS   # цвета и память уже перечислены в тексте модели
    p2 = ("Доступные варианты — " + "; ".join(e(x) for x in det) + ". ") if det and not has_text else ""
    p2 += (f"Все устройства новые и оригинальные, гарантия {months(wm)}. Заказ до 15:00 — доставим по Москве в тот же день "
           f"с 17:00 до 22:00, доставка {DELIVERY_COST} ₽; самовывоз бесплатно ({e(PICKUP)}). Оплата наличными при получении.")
    body = [crumbs, f"<h1>{e(full)}</h1>", f'<div class="lead"><p>{p1}</p></div>']
    if p["mems"]:
        body.append('<div class="chips">' + f'<a href="/catalog/{p["slug"]}/"{" class=on" if not mem else ""}>Все</a>' + "".join(
            f'<a href="/catalog/{p["slug"]}/{ms}/"{" class=on" if gb == mem else ""}>{mem_label(gb)}</a>'
            for ms, gb in p["mems"].items()) + "</div>")
    body.append(grid(its, f"/catalog.html#sub={quote(sub)}"))
    if not mem and n:
        body.append(f'<p class="more"><a class="btn" href="/catalog.html#sub={e(quote(sub))}">Выбрать и оформить заказ</a></p>')
    # уникальный текст — только на странице модели (на страницах памяти он был бы дублем)
    text_html, text_qa = model_text(m, p) if not mem else ("", [])
    if text_html:
        body.append(text_html)
    body.append(f'<h2>{"Условия покупки" if gen else "О покупке " + e(full) + " в ATOMM"}</h2><div class="lead"><p>{p2}</p></div>{facts_html(wm)}')
    qa = common_faq(f"«{full}»" if gen else full, its, wm)
    qa = qa[:1] + text_qa + qa[1:]
    fh, fld = faq_block(qa)
    body.append(fh)
    # соседние модели раздела — перелинковка
    sibs = [s for s in m["subs"] if m["sub_sec"][s] == p["sec"] and s != sub]
    if sub.startswith("Apple iPhone"):
        sibs = [s for s in sibs if s.startswith("Apple iPhone")] + [s for s in sibs if not s.startswith("Apple iPhone")]
    if sibs:
        body.append(f"<h2>Другие модели: {e(lower_first(p['sec']))}</h2>{models_list(m, sibs[:24])}")
    if gen:
        title = f"{full} — купить в Москве" + (f", цены от {rub(lo)}" if lo else "") + " | ATOMM"
    else:
        title = model_title(full, sub, ru, lo, bool(mem))
    avail = (f"{n} {plural(n, ['вариант', 'варианта', 'вариантов'])} в наличии" + (f" от {rub(lo)}" if lo else "")
             if n else "под заказ")
    desc = (f"{full}{alt}: {avail}. Только новая оригинальная техника, гарантия {wm} мес. "
            "Доставка по Москве сегодня при заказе до 15:00, оплата при получении.")
    img = next((it["img"] for it in st if it["img"]), None)
    return layout(title, desc, url, "\n".join(body), m,
                  crumbs_ld + fld + ("" if gen else agg_offer_ld(full, url, its, img, brand)),
                  robots=None if n else "noindex,follow", og_image=f"{BASE}/img/{img}" if img else None)


def page_product(m, iid):
    it = m["by_id"].get(iid)
    if not it:
        return None
    sub, sec = it["sub"], it["sec"]
    nm = short(it)
    wm = feed.warranty_months(sub)
    img = f"{BASE}/img/{it['img']}" if it["img"] else f"{BASE}/apple-touch-icon.png"
    avail = it["stock"]
    # раздел в крошках — раздел подраздела (как на странице подраздела), а не раздел самого товара
    trail = [(m["sub_sec"][sub], sec_url(m["sub_sec"][sub]))] if sub in m["sub_slug"] else [(sec, sec_url(sec))]
    if sub in m["sub_slug"]:
        trail.append((crumb_label(sub, m["sub_sec"][sub]), sub_url(m, sub)))
    trail.append((nm, None))
    crumbs, crumbs_ld = breadcrumbs(trail)
    ld = {"@context": "https://schema.org", "@type": "Product", "name": it["name"], "image": img, "sku": iid,
          "description": f"{it['name']}. Новый, оригинальный. Гарантия {months(wm)}.",
          "offers": {"@type": "Offer", "url": f"{BASE}/p/{iid}", "priceCurrency": "RUB", "price": it["price"],
                     "itemCondition": "https://schema.org/NewCondition",
                     "availability": "https://schema.org/InStock" if avail else "https://schema.org/OutOfStock",
                     "seller": {"@type": "Organization", "name": "ATOMM"}}}
    if it["brand"]:
        ld["brand"] = {"@type": "Brand", "name": it["brand"]}
    buy = (f'<a class="btn" href="/catalog.html#item-{e(iid)}">Купить</a>' if avail
           else '<a class="btn" href="/catalog.html" style="background:#8a8e94">Нет в наличии — в каталог</a>')
    price_txt = rub(it["price"]) if it["price"] else "Цена по запросу"
    rows = [("Состояние", "Новый, оригинал"), ("Наличие", "В наличии" if avail else "Нет в наличии")]
    if it["mem"]:
        rows.append(("Память", mem_label(it["mem"])))
    if it["color"]:
        rows.append(("Цвет", it["color"]))
    rows += [("Гарантия", f"{months(wm)} · возврат и обмен 14 дней"),
             ("Доставка", f"По Москве {DELIVERY_COST} ₽ — заказ до 15:00 привезём сегодня, с 17:00 до 22:00"),
             ("Самовывоз", f"Бесплатно: {PICKUP}"), ("Оплата", "Наличными при получении")]
    dl = "<dl>" + "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in rows) + "</dl>"
    badge = ""
    alt = ru_name(sub)
    body = [crumbs, f'<div class="pmain"><div class="big">{badge}<img src="{e(img)}" alt="{e(nm)}"></div><div>'
            f'<h1>{e(it["name"])}</h1><div class="price">{price_txt}</div>{buy}{dl}</div></div>']
    sibs = [x for x in m["sub_items"].get(sub, []) if x["id"] != iid]
    if sibs:
        hdr = (f"Другие товары: {e(display(sub, sec))}" if is_generic(sub)
               else f"Другие варианты {e(plain(sub))}{' (' + e(alt) + ')' if alt else ''}")
        body.append(f"<h2>{hdr}</h2>{grid(sibs[:24])}")
    title = f"{nm} — купить в Москве" + (f" за {price_txt}" if it["price"] else "") + " | ATOMM"
    desc = (f"{nm} — {price_txt}. Новый, оригинал, гарантия {months(wm)}. "
            "Доставка по Москве сегодня при заказе до 15:00 или бесплатный самовывоз. Оплата при получении.")
    return layout(title, desc, f"/p/{iid}", "\n".join(body), m, crumbs_ld + _ld(ld), og_image=img)


def render(m, slug, sub=None):
    """HTML страницы /catalog/<slug>/[<sub>/] или None (404)."""
    p = m["pages"].get(slug)
    if not p:
        return None
    if p["kind"] == "model":
        if sub:
            gb = p["mems"].get(sub)
            return page_model(m, p, gb) if gb else None
        return page_model(m, p)
    if sub:
        return None
    return page_group(m, p)


def _fill(tpl, ctx, escape):
    return tpl.format_map({k: (e(v) if escape else v) for k, v in ctx.items()})


def guide_url(slug):
    return f"/guides/{slug}/"


def page_guide(m, slug):
    """Статья /guides/<slug>/ из seo_content.GUIDES; цены и ссылки на память — из каталога."""
    g = seo_content.GUIDES.get(slug)
    if not g:
        return None
    url = guide_url(slug)
    models = [m["pages"].get(s) for s in g["models"]]
    models = [pg if pg and pg["kind"] == "model" else None for pg in models]
    ctx = {"lo_pro": "нет в наличии", "lo_max": "нет в наличии", "colors_sentence": ""}
    links = []
    for key, pg in zip(("pro", "max"), models):
        if not pg:
            continue
        v = variants_ctx(pg)
        if v["lo"]:
            ctx[f"lo_{key}"] = v["lo"]
        if v["colors"] and not ctx["colors_sentence"]:
            ctx["colors_sentence"] = f" В ATOMM сейчас есть: {v['colors']}."
        if in_stock(pg["items"]):
            nm = display(pg["sub"], pg["sec"])
            links.append(f'<p><a href="/catalog/{pg["slug"]}/">Все {e(nm)}</a>'
                         + (f" — по памяти: {v['mem_links'][0]}" if v["mem_links"][0] else "") + ".</p>")
    body_html = _fill(g["body"], ctx, True)
    if links:
        body_html += "<h2>Где посмотреть варианты</h2>" + "".join(links)
    crumbs, crumbs_ld = breadcrumbs([("iPhone", "/catalog/iphone/"), (g["title"], None)])
    src = "".join(f'<li><a href="{e(u)}" rel="nofollow noopener" target="_blank">{e(u)}</a></li>' for u in g["sources"])
    d = g["modified"]
    body = [crumbs, f"<h1>{e(g['title'])}</h1>", '<article class="article">',
            f'<p class="meta">Обновлено {d[8:10]}.{d[5:7]}.{d[:4]} · ATOMM</p>', body_html,
            f'<div class="src">Характеристики — по данным Apple и обзоров:<ul>{src}</ul></div></article>']
    for pg in models:
        if pg and in_stock(pg["items"]):
            body.append(f"<h2>{e(display(pg['sub'], pg['sec']))} в наличии</h2>"
                        + grid(sorted(in_stock(pg["items"]), key=lambda it: it["price"])[:8]))
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
          "inLanguage": "ru", "datePublished": g["published"], "dateModified": g["modified"],
          "mainEntityOfPage": BASE + url, "url": BASE + url,
          "author": {"@type": "Organization", "name": "ATOMM", "url": BASE + "/"},
          "publisher": {"@type": "Organization", "name": "ATOMM", "url": BASE + "/",
                        "logo": {"@type": "ImageObject", "url": BASE + "/icon-512.png"}},
          "about": [{"@type": "Product", "name": pg["sub"], "url": f"{BASE}/catalog/{pg['slug']}/"} for pg in models if pg]}
    img = next((it["img"] for pg in models if pg for it in in_stock(pg["items"]) if it["img"]), None)
    if img:
        ld["image"] = f"{BASE}/img/{img}"
    return layout(g["seo_title"], g["desc"], url, "\n".join(body), m, crumbs_ld + _ld(ld),
                  og_image=f"{BASE}/img/{img}" if img else None)


def not_found(m):
    body = ('<h1>Страница не найдена</h1><div class="lead"><p>Возможно, товар закончился или адрес изменился. '
            'Посмотрите <a href="/catalog/">каталог</a> или <a href="/catalog/iphone/">iPhone</a>.</p></div>')
    if m:
        body += f"<h2>Разделы</h2>{models_list(m, [s for s in m['subs'] if s.startswith('Apple iPhone')][:12])}"
    return layout("Страница не найдена | ATOMM", "Страница не найдена", None, body, m, robots="noindex,follow")


# ---------------------------------------------------------------- ссылки для статических страниц
def catalog_links(m):
    """Блок ссылок на разделы и модели — вставляется в catalog.html (виден и роботу, и людям)."""
    cols = []
    for sec in m["secs"]:
        subs = [s for s in m["subs"] if m["sub_sec"][s] == sec][:14]
        cols.append(f'<div><a class="h" href="{sec_url(sec)}">{e(sec)}</a>' + "".join(
            f'<a href="{sub_url(m, s)}">{e(display(s, sec))}</a>' for s in subs) + "</div>")
    return ('<section class="seo-links" aria-label="Разделы каталога"><style>'
            '.seo-links{max-width:1600px;margin:0 auto;padding:10px 32px 60px;display:grid;'
            'grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:22px;font-size:13px;color:#4a4e54}'
            '.seo-links a{display:block;text-decoration:none;padding:2px 0}.seo-links a:hover{text-decoration:underline}'
            '.seo-links a.h{font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;'
            'color:#1c1e21;margin-bottom:6px}@media(max-width:860px){.seo-links{padding:10px 18px 50px;grid-template-columns:1fr 1fr}}'
            '</style>' + "".join(cols) + "</section>")


# ---------------------------------------------------------------- sitemap
STATIC = [("/", "daily", "1.0"), ("/catalog.html", "daily", "0.8"), ("/delivery.html", "monthly", "0.4"),
          ("/warranty.html", "monthly", "0.4"), ("/contacts.html", "monthly", "0.5"),
          ("/offer.html", "yearly", "0.2"), ("/privacy.html", "yearly", "0.2")]


def sitemap(m):
    d = m["date"]
    urls = [(u, f, p) for u, f, p in STATIC]
    urls.append(("/catalog/", "daily", "0.9"))
    for sl, p in m["pages"].items():
        if p["kind"] in ("section", "collection"):
            urls.append((f"/catalog/{sl}/", "daily", "0.8"))
    for sl, p in m["pages"].items():
        if p["kind"] == "model" and in_stock(p["items"]):
            urls.append((f"/catalog/{sl}/", "daily", "0.9" if p["sub"].startswith("Apple iPhone") else "0.7"))
            for ms in p["mems"]:
                urls.append((f"/catalog/{sl}/{ms}/", "daily", "0.6"))
    for gs in seo_content.GUIDES:
        urls.append((guide_url(gs), "weekly", "0.6"))
    for it in m["items"]:
        if it["stock"] and it["cond"] == 0:
            urls.append((f"/p/{it['id']}", "daily", "0.5"))
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, f, p in urls:
        out.append(f"<url><loc>{BASE}{e(u)}</loc><lastmod>{d}</lastmod><changefreq>{f}</changefreq><priority>{p}</priority></url>")
    out.append("</urlset>")
    return "\n".join(out)
