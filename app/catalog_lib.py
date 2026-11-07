"""Общая логика каталога ATOMM: классификация товаров и сборка catalog.json."""
import hashlib
import json
import math
import os
import re
import tempfile
from datetime import datetime, timezone

DISCOUNT = float(os.environ.get("ATOMM_DISCOUNT", "0.005"))  # 0,5 %

SECTIONS = ["Смартфоны", "Планшеты", "Ноутбуки и компьютеры", "Часы и браслеты", "Аудио",
            "Игры и приставки", "Техника для дома и красоты", "Камеры и дроны", "Аксессуары"]

SERVICE_PREFIXES = ("Установка", "Перенос", "Настройка", "Пакет", "Срок", "Подарочная",
                    "Гравировка", "Пополнение", "Оплата", "Активация", "Техника в безопасности")

RULES = [
    (("Телефон",), "Смартфоны"),
    (("Планшет",), "Планшеты"),
    (("Ноутбук", "Моноблок", "Компьютер", "Монитор", "Мини-ПК", "Неттоп"), "Ноутбуки и компьютеры"),
    (("Умные часы", "Часы", "Фитнес-браслет", "Умное кольцо"), "Часы и браслеты"),
    (("Наушники", "Беспроводные наушники", "Беспроводной наушник", "Портативная", "Умная колонка",
      "Колонка", "Саундбар", "Беспроводная акустика"), "Аудио"),
    (("Игровая", "Игра", "Геймпад", "Портативная игровая"), "Игры и приставки"),
    (("Стайлер", "Фен", "Выпрямитель", "Пылесос", "Робот-пылесос", "Очиститель", "Моющий",
      "Увлажнитель", "Очиститель-увлажнитель", "Перкуссионный", "LED-маска", "Микротоковый",
      "Обогреватель", "Вентилятор"), "Техника для дома и красоты"),
    (("Экшн-камера", "Квадрокоптер", "Стабилизатор", "Камера"), "Камеры и дроны"),
]

TOP_FALLBACK = {
    "/aksessuary/": "Аксессуары", "/igrovye_pristavki/": "Игры и приставки", "/audio/": "Аудио",
    "/umniye_chasy_i_braslety/": "Часы и браслеты", "/kompyuternaya_tekhnika/": "Ноутбуки и компьютеры",
    "/planshety/": "Планшеты", "/telefony_apple/": "Смартфоны",
}

BRANDS = ["Apple", "Samsung", "Xiaomi", "Redmi", "Poco", "Huawei", "Honor", "Google", "Dyson", "Dreame",
          "Sony", "PlayStation", "Garmin", "Nintendo", "Lego", "Microsoft", "Nothing", "OnePlus", "JBL",
          "Marshall", "Pitaka", "Uniq", "Belkin", "Anker", "Baseus", "DJI", "GoPro", "Insta360", "Valve",
          "Meta", "ASUS", "Lenovo", "MSI", "Acer", "HP", "Яндекс", "Bang & Olufsen", "Bose", "Sennheiser",
          "Beats", "Spigen", "Native Union", "Satechi", "Ugreen", "Logitech", "Keychron", "Whoop", "Oura",
          "Amazfit", "Tecno", "Infinix", "Realme", "Vivo", "Oppo", "Hoco", "Deppa", "Laut", "Moft",
          "Mophie", "Zagg", "Nillkin", "ESR", "Switcheasy", "Incase", "Tomtoc", "Twelve South"]
BRAND_ALIAS = {"Redmi": "Xiaomi", "Poco": "Xiaomi", "PlayStation": "Sony"}
_BRAND_RE = [(b, re.compile(r"(?<![\w])" + re.escape(b) + r"(?![\w])", re.I)) for b in BRANDS]


def is_service(name):
    return name.startswith(SERVICE_PREFIXES)


# Не продаём: всё с маркой Store77, восстановленное, «Селект / как новое», уценку, их услуги и доработки
# (в т.ч. «русифицированные» клавиатуры MacBook), Lego.
EXCLUDED_SUBS = {"Store77 Outlet", "Восстановленная техника", "Техника Селект (как новая)", "Уцененная техника",
                 "Настройка компьютеров Mac", "Гравировка и клавиши", "Конструкторы Lego"}
_EXCLUDED_NAME = re.compile(r"store\s*77|стор\s*77|восстановлен|\(селект|селект\)|уценк|как нов|"
                            r"создание учетной записи|^конструктор|русифицирован", re.I)


def is_excluded(name, sub=""):
    return (sub in EXCLUDED_SUBS or "(Уценка)" in (sub or "") or bool(_EXCLUDED_NAME.search(name)))


def section_of(name, top):
    for keys, sec in RULES:
        if any(name.startswith(k) for k in keys):
            return sec
    return TOP_FALLBACK.get(top, "Аксессуары")


def brand_of(name):
    for b, rx in _BRAND_RE:
        if rx.search(name):
            return BRAND_ALIAS.get(b, b)
    return ""


def cond_of(name):
    if "Селект" in name:
        return 1
    if re.search(r"уцен", name, re.I):
        return 2
    return 0


def our_price(p):
    return int(math.floor(p * (1 - DISCOUNT))) if p else 0


def product_id(url_path):
    slug = url_path.strip("/").split("/")[-1]
    return hashlib.sha1(slug.encode()).hexdigest()[:10]


def build(products):
    """products: list of dict(url, name, price, in_stock, sub_name, top)."""
    goods = []
    for p in products:
        if is_service(p["name"]) or is_excluded(p["name"], p.get("sub_name") or ""):
            continue
        goods.append(dict(id=product_id(p["url"]), section=section_of(p["name"], p.get("top", "")),
                          brand=brand_of(p["name"]), sub=p.get("sub_name") or "Прочее", name=p["name"],
                          price=our_price(p.get("price")), stock=1 if p.get("in_stock") else 0,
                          cond=cond_of(p["name"])))
    seniority_sort(goods, lambda g: (SECTIONS.index(g["section"]), g["brand"], g["name"], g["price"]))
    brands = sorted({g["brand"] for g in goods if g["brand"]})
    subs = order_subs(g["sub"] for g in goods)  # в порядке старшинства товаров
    bi = {b: i for i, b in enumerate(brands)}
    si = {s: i for i, s in enumerate(subs)}
    items = [[g["id"], SECTIONS.index(g["section"]), bi.get(g["brand"], -1), si[g["sub"]], g["name"],
              g["price"], g["stock"], g["cond"]] for g in goods]
    return {"v": datetime.now(timezone.utc).isoformat(timespec="minutes"), "sections": SECTIONS,
            "brands": brands, "subs": subs, "items": items}


def write_atomic(data, path):
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".catalog-", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    os.chmod(tmp, 0o644)
    os.replace(tmp, path)


# ---------- порядок «по старшинству» ----------
BRAND_ORDER = ["Apple", "Samsung", "Xiaomi", "Huawei", "Honor", "Google", "Nothing", "OnePlus", "Sony", "Dyson"]
_TIERS = [(re.compile(r"pro\s*max|ultra", re.I), 5), (re.compile(r"\bpro\b", re.I), 4),
          (re.compile(r"\bair\b", re.I), 3), (re.compile(r"\bplus\b|\d\+", re.I), 2),
          (re.compile(r"\bfe\b|\blite\b|\bmini\b|\bneo\b", re.I), 0.5)]
_MEM = re.compile(r"(\d+)\s*/\s*(\d+)\s*(гб|тб|gb|tb)|(\d+(?:[.,]\d+)?)\s*(гб|тб|gb|tb|мм|mm|\"|дюйм)", re.I)


def model_info(name):
    """(семейство, поколение, линейка, память ГБ) из названия товара."""
    n = name.lower().replace("ё", "е").replace("м", "m") if re.search(r"\bм\d", name.lower()) else name.lower().replace("ё", "е")
    core = re.split(r",|\(|цвет", n)[0]
    storage = 0
    for m in _MEM.finditer(core):
        if m.group(3):
            storage = int(m.group(2)) * (1024 if m.group(3).lower() in ("тб", "tb") else 1)
        elif m.group(5) and m.group(5).lower() in ("гб", "тб", "gb", "tb"):
            v = float(m.group(4).replace(",", "."))
            storage = int(v * (1024 if m.group(5).lower() in ("тб", "tb") else 1))
    plain = _MEM.sub(" ", core)
    year = re.search(r"\((20\d\d)\)", n)
    chip = re.search(r"\bm(\d)\b", re.split(r"цвет", n)[0])
    num = re.search(r"(?<![\d.])(\d{1,4})(e)?(?![\d.])", plain)
    tier = 1.0
    for rx, t in _TIERS:
        if rx.search(plain):
            tier = t
            break
    if year:
        gen = int(year.group(1))
    elif chip:
        gen = int(chip.group(1))
    elif num:
        gen = int(num.group(1))
        if num.group(2):
            tier = 0.0  # iPhone 16e / 17e — младшая модель поколения
    elif "iphone air" in plain:
        gen, tier = 17, 3.0
    else:
        gen = 0
    family = re.sub(r"\d+e\b|\d+|pro\s*max|ultra|\bpro\b|\bair\b|\bplus\b|\bfe\b|\blite\b|\bmini\b|\+", " ", plain)
    family = " ".join(family.split())
    return family, gen, tier, storage


def seniority_sort(rows, get):
    """rows — любые записи; get(row) -> (section_index, brand, name, price). Сортирует на месте."""
    infos = {}
    fam_top = {}
    for r in rows:
        sec, brand, name, price = get(r)
        fam, gen, tier, mem = model_info(name)
        infos[id(r)] = (fam, gen, tier, mem)
        k = (sec, brand, fam)
        fam_top[k] = max(fam_top.get(k, 0), price or 0)

    def key(r):
        sec, brand, name, price = get(r)
        fam, gen, tier, mem = infos[id(r)]
        bo = BRAND_ORDER.index(brand) if brand in BRAND_ORDER else (len(BRAND_ORDER) if brand else 999)
        return (sec, bo, brand, -fam_top[(sec, brand, fam)], fam, -gen, -tier, mem, price or 0, name)

    rows.sort(key=key)
    return rows


def order_subs(subs_in_item_order):
    """Подразделы по старшинству товаров; общие («Телефоны», «Аксессуары» — без латиницы и цифр) — в конец."""
    subs = list(dict.fromkeys(subs_in_item_order))
    generic = [x for x in subs if not re.search(r"[A-Za-z0-9]", x)]
    return [x for x in subs if x not in generic] + generic
