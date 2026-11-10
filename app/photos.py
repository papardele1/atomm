"""Официальные фото товаров ATOMM.

Для каждой пары «модель + цвет» ищем картинку в Яндекс.Картинках только на сайте производителя
(site:apple.com и т. п.), скачиваем несколько кандидатов и берём предметную съёмку: название модели
и цвета в адресе/подписи, белый или прозрачный фон, без баннеров и интерьерных кадров.
Результат: /www/img/<hash>.webp и /www/img/index.json {id товара: файл}. Работает медленно
и вежливо (пауза между запросами), прогресс сохраняется, перезапуск продолжает с места остановки.

Запуск:  python app/photos.py --loop            — постоянный сервис (добирает новые товары)
         python app/photos.py --sample 40 --out /tmp/job-out   — пробный прогон с контактным листом
"""

import argparse
import hashlib
import html
import io
import json
import logging
import os
import random
import re
import sys
import time
from urllib.parse import urlparse

import requests
from PIL import Image, ImageDraw

log = logging.getLogger("photos")
CATALOG = os.environ.get("ATOMM_CATALOG", "/www/catalog.json")
IMG_DIR = os.environ.get("ATOMM_IMG", os.path.join(os.path.dirname(CATALOG), "img"))
STATE = os.path.join(IMG_DIR, "keys.json")
INDEX = os.path.join(IMG_DIR, "index.json")
PAUSE = float(os.environ.get("PHOTO_PAUSE", "4"))
RETRY_MISS_DAYS = 7

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8"})

# Бренд → официальные сайты (для site:) и хосты, с которых принимаем картинки.
SITES = {
    "Apple": (["apple.com"], ["apple.com", "cdn-apple.com"]),
    "Beats": (["beatsbydre.com", "apple.com"], ["beatsbydre.com", "apple.com", "cdn-apple.com"]),
    "Samsung": (["samsung.com"], ["samsung.com"]),
    "Xiaomi": (["mi.com"], ["mi.com", "appmifile.com", "xiaomi.com"]),
    "Huawei": (["consumer.huawei.com"], ["huawei.com", "hicloud.com"]),
    "Honor": (["honor.com"], ["honor.com", "hihonor.com"]),
    "Google": (["store.google.com"], ["google.com", "googleusercontent.com", "gstatic.com"]),
    "Nothing": (["nothing.tech"], ["nothing.tech", "shopify.com"]),
    "OnePlus": (["oneplus.com"], ["oneplus.com", "oneplus.net"]),
    "Sony": (["sony.com", "sony.ru"], ["sony.com", "sony.ru", "scene7.com", "sony.net"]),
    "Dyson": (["dyson.com", "dyson.co.uk"], ["dyson.com", "dyson.co.uk", "dyson.ru", "dyson.cn"]),
    "Garmin": (["garmin.com"], ["garmin.com"]),
    "JBL": (["jbl.com"], ["jbl.com", "harman.com"]),
    "Marshall": (["marshall.com"], ["marshall.com", "marshallheadphones.com"]),
    "Nintendo": (["nintendo.com"], ["nintendo.com", "nintendo.net"]),
    "GoPro": (["gopro.com"], ["gopro.com"]),
    "DJI": (["dji.com"], ["dji.com", "djicdn.com"]),
    "Insta360": (["insta360.com"], ["insta360.com"]),
    "Ugreen": (["ugreen.com"], ["ugreen.com"]),
    "Baseus": (["baseus.com"], ["baseus.com"]),
    "Satechi": (["satechi.net"], ["satechi.net", "shopify.com"]),
    "Pitaka": (["pitakaglobal.com", "pitaka.com"], ["pitaka", "shopify.com"]),
    "Uniq": (["uniq-store.com", "uniqstore.com"], ["uniq", "shopify.com"]),
    "Whoop": (["whoop.com"], ["whoop.com"]),
    "MSI": (["msi.com"], ["msi.com"]),
    "ASUS": (["asus.com"], ["asus.com"]),
    "Microsoft": (["microsoft.com", "xbox.com"], ["microsoft.com", "xbox.com", "s-microsoft.com"]),
    "Lenovo": (["lenovo.com"], ["lenovo.com"]),
    "HP": (["hp.com"], ["hp.com"]),
    "Acer": (["acer.com"], ["acer.com"]),
    "Dreame": (["dreametech.com", "dreame.tech"], ["dreame"]),
    "Яндекс": (["yandex.ru"], ["yandex.ru", "yandex.net", "yastatic.net"]),
    "Amazfit": (["amazfit.com"], ["amazfit.com", "zepp.com"]),
    "Bose": (["bose.com"], ["bose.com", "bose.ru"]),
    "Sennheiser": (["sennheiser.com"], ["sennheiser.com"]),
    "Logitech": (["logitech.com"], ["logitech.com", "logitechg.com"]),
    "Realme": (["realme.com"], ["realme.com"]),
    "Vivo": (["vivo.com"], ["vivo.com"]),
    "Oppo": (["oppo.com"], ["oppo.com"]),
    "Meta": (["meta.com"], ["meta.com", "fbcdn.net"]),
    "Valve": (["steamdeck.com", "steampowered.com"], ["steamdeck.com", "steampowered.com", "steamstatic.com"]),
    "Bowers & Wilkins": (["bowerswilkins.com"], ["bowerswilkins.com", "bowerswilkins"]),
    "Tomtoc": (["tomtoc.com"], ["tomtoc"]),
    "Native Union": (["nativeunion.com"], ["nativeunion"]),
    "VLP": (["vlp.ru"], ["vlp.ru", "vlp"]),
    "Gurdini": (["gurdini.ru"], ["gurdini"]),
    "Remax": (["remax.ru", "remaxofficial.com"], ["remax"]),
    "Elago": (["elago.com"], ["elago"]),
    "Wiwu": (["wiwu.net", "wiwu.ru"], ["wiwu"]),
    "UAG": (["urbanarmorgear.com"], ["urbanarmorgear", "uag"]),
    "uBear": (["ubear.ru"], ["ubear"]),
    "Dux": (["duxducis.com"], ["duxducis"]),
    "SanDisk": (["westerndigital.com", "sandisk.com"], ["westerndigital.com", "sandisk.com", "wdc.com"]),
    "Harman Kardon": (["harmankardon.com"], ["harmankardon", "harman.com"]),
    "Magssory": (["magssory.com"], ["magssory"]),
    "PlayStation": (["playstation.com"], ["playstation.com", "playstation.net", "sony.com", "scene7.com"]),
}
ALIASES = {"redmi": "Xiaomi", "poco": "Xiaomi", "xiaomi": "Xiaomi", "iphone": "Apple", "ipad": "Apple", "macbook": "Apple",
           "airpods": "Apple", "imac": "Apple", "playstation": "PlayStation", "ps5": "PlayStation", "dualsense": "PlayStation",
           "xbox": "Microsoft", "steam": "Valve", "switch": "Nintendo", "joy-con": "Nintendo", "galaxy": "Samsung",
           "pixel": "Google", "oculus": "Meta", "quest": "Meta", "bowers": "Bowers & Wilkins", "tomtoc": "Tomtoc",
           "native": "Native Union", "sandisk": "SanDisk", "harman": "Harman Kardon", "apple": "Apple", "samsung": "Samsung"}

BAD = re.compile(r"hero|banner|lifestyle|newsroom|blog|header|/kv|keyvisual|key-visual|wallpaper|video|texture|feature|startframe|"
                 r"compare|social|og[-_]image|og\.|share|campaign|promo|bg[-_]|background|logo|icon|sprite|_sw_color|swatch|"
                 r"1600x864|1440x|1920x|2560x|community|forum|thumb_|/tile/|reviews?/|event", re.I)
GOOD = re.compile(r"gallery|product|finish|pdp|packshot|front|png-alpha|fmt=png|witb|/list-|catalog|sku|item|/p6pim/|static", re.I)

CYR = re.compile(r"[А-Яа-яЁё]")
_EN_COLOR = re.compile(r"\(([A-Za-z][A-Za-z0-9 \-/+&']{2,40})\)")


def norm(s):
    return re.sub(r"[^a-z0-9а-яё]", "", s.lower())


def accessory_maker(name):
    """Для аксессуара «X для <устройство>» бренд — производитель аксессуара (X), а не устройства.
    Возвращает None, если это не аксессуар; '' — если производитель не указан."""
    m = re.match(r"(.*?)\s+для\s+", name, re.I)
    if not m:
        return None
    toks = re.findall(r"[A-Za-z][A-Za-z0-9\-]+", m.group(1))
    return toks[0] if toks else ""


def brand_of(name, brand):
    """Бренд самого товара: из каталога, иначе первое латинское слово модели («Remax iPhone 16» → Remax,
    а не Apple — иначе для чехла стороннего бренда нашлась бы картинка Apple)."""
    if re.search(r"dualsense|dualshock|playstation portal|ps vr", name, re.I):
        return "PlayStation"
    acc = None if re.match(r"(игра|диск)\b", name, re.I) else accessory_maker(name)
    if acc is not None:
        if not acc:
            return ""
        t = acc.lower()
        if t in ALIASES:
            return ALIASES[t]
        return next((k for k in SITES if k.lower() == t), acc)
    if brand and brand in SITES:
        return brand
    if re.match(r"(игра|диск)\b", name, re.I):  # игры — по платформе
        for pat, b in ((r"ps5|ps4|playstation", "PlayStation"), (r"switch", "Nintendo"), (r"xbox", "Microsoft")):
            if re.search(pat, name, re.I):
                return b
    toks = re.findall(r"[A-Za-z][A-Za-z0-9\-]+", model_of(name))
    if toks:
        t = toks[0].lower()
        if t in ALIASES:
            return ALIASES[t]
        for k in SITES:
            if t == k.lower():
                return k
        if not brand:
            return toks[0]
    return brand or ""


def model_of(name):
    """Латинская часть названия до первой запятой/скобки, без памяти: «Apple iPhone 17 Pro Max»."""
    n = re.split(r"[,(]", name, 1)[0]
    n = re.sub(r"\b\d+\s*/\s*\d+\s*(ГБ|ТБ|GB|TB)\b|\b\d+\s*(ГБ|ТБ|GB|TB|Gb|Tb)\b", " ", n, flags=re.I)
    toks = [t for t in n.split() if not CYR.search(t)]
    return " ".join(toks).strip(" -–\"")


def color_of(name):
    """(английское название цвета или None, русское или None)."""
    en = ru = None
    m = re.search(r"(?:цвет|корпус):?\s+([^,(]+)(?:\(([^)]+)\))?", name, re.I)
    if m:
        ru = m.group(1).strip()
        if m.group(2) and not CYR.search(m.group(2)):
            en = m.group(2).strip()
    if not en:
        for c in _EN_COLOR.findall(name):  # первый подходящий: у часов это цвет корпуса, а не ремешка
            if not re.search(r"\d{2,}|gb|tb|ssd|wi-?fi|lte|gps|cellular|esim|sim|m\d|intel|amd|ryzen|core|rtx", c, re.I):
                en = c.strip()
                break
    if en and re.fullmatch(r"[A-Z0-9]{4,8}(/[A-Z])?", en) and re.search(r"\d", en):  # код модели (MW1G3), не цвет
        en = None
    if not ru:
        m = re.search(r"\)\s*([А-Яа-яЁё][А-Яа-яЁё\- ]+?)\s*(?:\(|[A-Z0-9]{4,}|$)", name)
        if m:
            ru = m.group(1).strip()
    if not ru:
        ps = re.findall(r"\(([А-Яа-яЁё][А-Яа-яЁё\- ]{2,25})\)", name)
        if ps:
            ru = ps[-1]
    return en, ru


def key_of(name, brand):
    b = brand_of(name, brand)
    en, ru = color_of(name)
    return f"{b}|{model_of(name)}|{(en or ru or '').lower()}", b, en, ru


# ---------------- поиск ----------------
_ITEM = re.compile(r'"alt":"((?:[^"\\]|\\.)*)","width":\d+,"height":\d+,"origWidth":(\d+),"origHeight":(\d+),'
                   r'"origUrl":"((?:[^"\\]|\\.)*)","snippet":\{"title":"(?:[^"\\]|\\.)*","domain":"([^"]*)"')


class Captcha(Exception):
    pass


def yandex(query):
    r = S.get("https://yandex.ru/images/search", params={"text": query}, timeout=20)
    h = html.unescape(r.text)
    if "smartcaptcha" in h.lower() or "showcaptcha" in r.url:
        raise Captcha()
    out = []
    for alt, w, hh, url, dom in _ITEM.findall(h):
        try:
            url = json.loads(f'"{url}"')
            alt = json.loads(f'"{alt}"')
        except ValueError:
            continue
        out.append({"alt": alt, "w": int(w), "h": int(hh), "url": url, "dom": dom})
    return out


def official(c, brand):
    hosts = SITES.get(brand, ([], []))[1] or [brand.lower()]

    def ok(host):
        host = host.lower().split(":")[0]
        for x in hosts:
            if "." in x:
                if host == x or host.endswith("." + x):
                    return True
            elif x in host:  # имя бренда без домена (pitaka, uniq…)
                return True
        return False
    return ok(urlparse(c["url"]).netloc) or ok(c["dom"])


COLORS = ["black", "white", "silver", "gray", "grey", "gold", "blue", "green", "red", "pink", "purple", "violet", "yellow",
          "orange", "brown", "beige", "navy", "lavender", "titanium", "graphite", "midnight", "starlight", "teal", "mint",
          "черн", "бел", "серебр", "сер", "золот", "син", "голуб", "зелен", "красн", "розов", "фиолет", "желт",
          "оранж", "коричн", "бежев", "лаванд", "титан", "графит", "бирюз", "мят"]


def color_tokens(en, ru):
    t = set()
    for col in (en, ru):
        if col:
            for w in re.findall(r"[a-zа-яё]+", col.lower()):
                for c in COLORS:
                    if w.startswith(c):
                        t.add(c)
    return t


def url_score(c, model, en, ru):
    text = norm(c["url"] + " " + c["alt"])
    s = 0
    toks = [t for t in re.findall(r"[a-z0-9]+", model.lower()) if t not in ("apple", "samsung", "xiaomi", "galaxy", "huawei", "sony")]
    s += sum(2 for t in toks if t in text)
    exact = any(col and norm(col) and norm(col) in text for col in (en, ru))
    want = color_tokens(en, ru)
    seen = {c for c in COLORS if c in text}
    if exact:
        s += 5
    elif want and (want & seen):
        s += 3
    elif want and seen:
        s -= 7  # на картинке, судя по подписи, другой цвет
    elif want:
        s -= 2
    if BAD.search(c["url"]):
        s -= 6
    if GOOD.search(c["url"]):
        s += 2
    r = c["w"] / max(c["h"], 1)
    s += 2 if 0.55 <= r <= 1.8 else (-5 if r > 2.2 or r < 0.4 else 0)
    if max(c["w"], c["h"]) < 300:
        s -= 4
    return s


GENERIC = {"apple", "samsung", "xiaomi", "galaxy", "huawei", "sony", "for", "with", "and", "the", "playstation", "nintendo",
           "switch", "ps5", "ps4", "magsafe", "case", "pro", "max", "plus", "mini", "ultra", "air"}


def coverage(c, model):
    """Доля значимых слов модели (Gothic, Remake, F8, s26…), найденных в адресе или подписи картинки."""
    toks = [t for t in re.findall(r"[a-z0-9]+", model.lower()) if t not in GENERIC and len(t) > 1]
    if not toks:
        return 1.0
    text = norm(c["url"] + " " + c["alt"])
    return sum(1 for t in toks if t in text) / len(toks)


def fetch_img(url):
    r = S.get(url, timeout=25, headers={"Referer": "https://yandex.ru/"})
    r.raise_for_status()
    im = Image.open(io.BytesIO(r.content))
    im.load()
    return im


def trim(im):
    """Обрезает поля (прозрачные или цвета фона по углам), оставляя 4% отступа."""
    im = im.convert("RGBA")
    a = im.getchannel("A")
    box = a.point(lambda v: 255 if v > 20 else 0).getbbox()
    if box:
        im = im.crop(box)
    w, h = im.size
    rgb = im.convert("RGB")
    corners = [rgb.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    bg = tuple(sorted(c[i] for c in corners)[1] for i in range(3))
    from PIL import ImageChops
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, bg)).convert("L").point(lambda v: 255 if v > 24 else 0)
    alpha = im.getchannel("A").point(lambda v: 255 if v > 20 else 0)
    mask = ImageChops.multiply(diff, alpha)
    box = mask.getbbox()
    if box:
        pad = int(max(box[2] - box[0], box[3] - box[1]) * 0.04)
        box = (max(0, box[0] - pad), max(0, box[1] - pad), min(w, box[2] + pad), min(h, box[3] + pad))
        frac = (box[2] - box[0]) * (box[3] - box[1]) / max(w * h, 1)
        im = im.crop(box)
    else:
        frac = 0
    return im, frac


def packshot_score(im):
    """Доля «чистого» края кадра: белый/светло-серый или прозрачный фон — признак предметной съёмки."""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    pts = [(x, y) for x in range(0, w, max(1, w // 40)) for y in (0, h - 1)] + \
          [(x, y) for y in range(0, h, max(1, h // 40)) for x in (0, w - 1)]
    clean = 0
    for x, y in pts:
        r, g, b, a = px[min(x, w - 1), min(y, h - 1)]
        if a < 30 or (r > 215 and g > 215 and b > 215 and max(r, g, b) - min(r, g, b) < 18):
            clean += 1
    return clean / max(len(pts), 1)


def remove_bg(im):
    """Делает однотонный светлый фон кадра прозрачным (заливка от краёв), чтобы товар лежал на сером фоне сайта."""
    from PIL import ImageChops, ImageFilter
    im = im.convert("RGBA")
    w, h = im.size
    rgb = im.convert("RGB")
    corners = [rgb.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    bg = tuple(sorted(c[i] for c in corners)[1] for i in range(3))
    if min(bg) < 200 or max(bg) - min(bg) > 20:  # фон не светлый однотонный — не трогаем
        return im
    near = ImageChops.difference(rgb, Image.new("RGB", rgb.size, bg)).convert("L").point(lambda v: 255 if v < 14 else 0)
    step = max(1, min(w, h) // 60)
    for x in range(0, w, step):
        for y in (0, h - 1):
            if near.getpixel((x, y)) == 255:
                ImageDraw.floodfill(near, (x, y), 128)
    for y in range(0, h, step):
        for x in (0, w - 1):
            if near.getpixel((x, y)) == 255:
                ImageDraw.floodfill(near, (x, y), 128)
    mask = near.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.GaussianBlur(0.8))
    im.putalpha(ImageChops.multiply(im.getchannel("A"), mask))
    return im


def save(im, key):
    os.makedirs(IMG_DIR, exist_ok=True)
    im = remove_bg(im.convert("RGBA"))
    im.thumbnail((900, 900), Image.LANCZOS)
    fn = hashlib.sha1(key.encode()).hexdigest()[:14] + ".webp"
    im.save(os.path.join(IMG_DIR, fn), "WEBP", quality=82, method=5)
    return fn


STRICT_COLOR = {"Смартфоны", "Планшеты", "Часы и браслеты", "Ноутбуки и компьютеры"}


def find(name, brand_name, sec=""):
    key, b, en, ru = key_of(name, brand_name)
    model = model_of(name)
    if not model or b not in SITES:
        return key, None, "нет официального сайта бренда"
    sites = SITES[b][0]
    tried = []
    col = en or ru or ""
    chip = re.search(r"\((M\d(?:\s+(?:Pro|Max|Ultra))?|A\d\d\s*Pro)\b", name.replace("М", "M"))
    qmodel = f"{model} {chip.group(1)}" if chip else model
    strict = sec in STRICT_COLOR and bool(color_tokens(en, ru) or en)
    queries = [f"{qmodel} {col}".strip()] + ([qmodel] if col and not strict else [])
    for q in queries:
        for site in sites[:2]:
            cands = [c for c in yandex(f"{q} site:{site}") if official(c, b)]
            time.sleep(PAUSE + random.random() * 2)
            cands.sort(key=lambda c: url_score(c, qmodel, en, ru), reverse=True)
            best = None
            for c in cands[:5]:
                sc = url_score(c, qmodel, en, ru)
                if sc < 1:
                    continue
                if coverage(c, model) < 0.5:  # в подписи/адресе должна быть хотя бы половина названия модели
                    continue
                if strict:  # цвет должен подтверждаться адресом или подписью картинки
                    text = norm(c["url"] + " " + c["alt"])
                    if not (any(x and norm(x) and norm(x) in text for x in (en, ru)) or (color_tokens(en, ru) & {k for k in COLORS if k in text})):
                        continue
                if chip and not re.search(re.escape(chip.group(1).replace(" ", "").lower()), norm(c["url"] + " " + c["alt"])) and \
                        re.search(r"\bm\d\b", (c["url"] + " " + c["alt"]).lower()):
                    continue  # на картинке явно другой чип
                try:
                    im = fetch_img(c["url"])
                except Exception:  # noqa: BLE001
                    continue
                if min(im.size) < 200:
                    continue
                ps_raw = packshot_score(im)  # фон по краям исходного кадра
                im, frac = trim(im)
                if min(im.size) < 160 or frac < 0.05:  # товар — крошечная часть баннера
                    continue
                ps = ps_raw
                total = sc + 8 * ps
                if q == model and col:  # без цвета — только если картинка явно предметная
                    total -= 3
                if not best or total > best[0]:
                    best = (total, im, c["url"], ps)
            tried.append(len(cands))
            if best and best[3] >= 0.6 and best[0] >= 8:
                return key, best, None
    return key, None, f"не найдено (кандидатов: {tried})"


# ---------------- состояние ----------------
def load_state():
    try:
        with open(STATE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, path)


def catalog_items():
    with open(CATALOG) as f:
        d = json.load(f)
    for r in d["items"]:
        yield r[0], r[4], d["brands"][r[2]] if r[2] >= 0 else "", d["sections"][r[1]]


def rebuild_index(state):
    idx = {}
    for iid, name, brand, _ in catalog_items():
        k = key_of(name, brand)[0]
        f = state.get(k, {}).get("f")
        if f:
            idx[iid] = f
    os.makedirs(IMG_DIR, exist_ok=True)
    write_json(INDEX, idx)
    return len(idx)


def todo(state):
    seen, out = set(), []
    for iid, name, brand, sec in catalog_items():
        k = key_of(name, brand)[0]
        if k in seen:
            continue
        seen.add(k)
        st = state.get(k)
        if st and (st.get("f") or st.get("block") or time.time() - st.get("t", 0) < RETRY_MISS_DAYS * 86400):
            continue
        out.append((k, name, brand, sec))
    return out


URLS = os.path.join(os.path.dirname(CATALOG), "urls.json")
_OG = re.compile(r'<meta property="og:image" content="([^"]+)"')


def fill_from_store(limit=None):
    """Фото для товаров, у которых их ещё нет: главная картинка карточки Store77 (og:image) — каталог взят оттуда,
    поэтому фото точно той же модели и цвета. Фон делаем прозрачным (серый фон сайта), как у остальных фото."""
    try:
        with open(URLS) as f:
            urls = json.load(f)
    except (OSError, ValueError):
        log.info("нет urls.json — пропускаю фото со Store77")
        return 0
    sys.path.insert(0, os.path.dirname(__file__))
    import parser as store  # сессия и обход защиты Store77
    state = load_state()
    seen, work = set(), []
    for iid, name, brand, sec in catalog_items():
        k = key_of(name, brand)[0]
        if k in seen:
            continue
        seen.add(k)
        st = state.get(k) or {}
        if st.get("f") or st.get("block") or st.get("s77_miss", 0) > time.time() - 3 * 86400 or iid not in urls:
            continue
        work.append((k, iid, name))
    log.info("фото со Store77: к обработке %d ключей", len(work))
    got = 0
    for n, (k, iid, name) in enumerate(work[:limit] if limit else work):
        try:
            h = store.get(store.BASE + urls[iid])
            m = _OG.search(h or "")
            if not m or "nophoto" in m.group(1).lower() or "no_photo" in m.group(1).lower():
                raise ValueError("нет og:image")
            r = store.session.get(m.group(1), timeout=30)
            r.raise_for_status()
            im = Image.open(io.BytesIO(r.content))
            im.load()
            if min(im.size) < 200:
                raise ValueError(f"маленькое фото {im.size}")
            im, frac = trim(im)
            fn = save(im, k)
            cur = load_state()  # фото могли добавить параллельно — перечитываем перед записью
            cur[k] = {"f": fn, "u": m.group(1), "t": int(time.time()), "src": "store77"}
            state = cur
            got += 1
            log.info("✓ store77 %s", name[:80])
        except Exception as e:  # noqa: BLE001
            cur = load_state()
            cur.setdefault(k, {})["s77_miss"] = int(time.time())
            cur[k]["why_s77"] = str(e)[:120]
            state = cur
            log.info("✗ store77 %s — %s", name[:70], e)
        write_json(STATE, state)
        if n % 20 == 19:
            rebuild_index(state)
        time.sleep(0.6 + random.random() * 0.8)
    rebuild_index(load_state())
    log.info("фото со Store77: добавлено %d", got)
    return got


def _merge(state, changed):
    """Записать только свои изменения поверх файла: фото могли добавить параллельно (Store77, ручные)."""
    cur = load_state()
    for k in changed:
        if (cur.get(k) or {}).get("f") and not state[k].get("f"):
            continue  # кто-то уже нашёл фото — не затираем промахом
        cur[k] = state[k]
    write_json(STATE, cur)
    return cur


def run(limit=None, sample=None):
    if not sample:
        fill_from_store(limit)
    state = load_state()
    work = todo(state)
    if sample:
        random.seed(7)
        by = {}
        for w in work:
            by.setdefault(w[3], []).append(w)
        work = []
        while len(work) < sample and any(by.values()):
            for sec in list(by):
                if by[sec] and len(work) < sample:
                    work.append(by[sec].pop(random.randrange(len(by[sec]))))
    log.info("к обработке: %d ключей", len(work) if not limit else min(limit, len(work)))
    done, changed = [], set()
    for n, (k, name, brand, sec) in enumerate(work[:limit] if limit else work):
        try:
            key, best, why = find(name, brand, sec)
        except Captcha:
            log.warning("капча Яндекса — пауза 15 минут")
            time.sleep(900)
            continue
        except Exception as e:  # noqa: BLE001
            log.warning("%s: %s", name[:60], e)
            continue
        if best:
            fn = save(best[1], key)
            state[key] = {"f": fn, "u": best[2], "t": int(time.time())}
            changed.add(key)
            log.info("✓ %s → %s (%.1f, фон %.0f%%)", name[:70], urlparse(best[2]).netloc, best[0], best[3] * 100)
        else:
            state[key] = {**{x: y for x, y in state.get(key, {}).items() if x.startswith(("s77", "why_s77"))}, "t": int(time.time()), "why": why}
            changed.add(key)
            log.info("✗ %s — %s", name[:70], why)
        done.append((name, sec, state[key]))
        if n % 10 == 9:
            state = _merge(state, changed)
            rebuild_index(state)
    state = _merge(state, changed)
    log.info("в индексе товаров с фото: %d", rebuild_index(state))
    return done


def contact_sheet(done, out):
    os.makedirs(out, exist_ok=True)
    cols, cw, ch = 6, 220, 270
    rows = (len(done) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, max(rows, 1) * ch), "white")
    d = ImageDraw.Draw(sheet)
    lines = []
    for i, (name, sec, st) in enumerate(done):
        x, y = (i % cols) * cw, (i // cols) * ch
        if st.get("f"):
            im = Image.open(os.path.join(IMG_DIR, st["f"])).convert("RGBA")
            im.thumbnail((200, 200))
            bg = Image.new("RGB", im.size, (236, 237, 239))
            bg.paste(im, mask=im.getchannel("A"))
            sheet.paste(bg, (x + 10, y + 8))
        else:
            d.rectangle([x + 10, y + 8, x + 210, y + 208], outline=(200, 80, 80))
            d.text((x + 70, y + 100), "НЕТ ФОТО", fill=(200, 80, 80))
        d.text((x + 8, y + 214), f"{i + 1}. {name[:30]}", fill=(0, 0, 0))
        d.text((x + 8, y + 230), name[30:60], fill=(0, 0, 0))
        lines.append(f"{i + 1}. [{sec}] {name} -> {st.get('u') or st.get('why')}")
    sheet.save(os.path.join(out, "sheet.jpg"), quality=80)
    with open(os.path.join(out, "sheet.txt"), "w") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loop", action="store_true")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--sample", type=int)
    ap.add_argument("--out", default="/tmp/job-out")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stdout)
    if a.sample:
        contact_sheet(run(sample=a.sample), a.out)
        return
    while True:
        run(limit=a.limit)
        if not a.loop:
            break
        time.sleep(3600)


if __name__ == "__main__":
    main()
