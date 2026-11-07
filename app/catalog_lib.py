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
          (re.compile(r"\bfe\+", re.I), 0.8), (re.compile(r"\bfe\b", re.I), 0.6),
          (re.compile(r"\blite\b|\bmini\b|\bneo\b", re.I), 0.5)]
_MEM = re.compile(r"(\d+)\s*/\s*(\d+)\s*(гб|тб|gb|tb)|(\d+(?:[.,]\d+)?)\s*(гб|тб|gb|tb|мм|mm|\"|дюйм)", re.I)


# Линейки, где номер модели не равен поколению: переводим в год выхода,
# чтобы «сначала новые, потом по старшинству» работало внутри всей линейки.
_IPAD_CHIP_YEAR = {"pro": {5: 2025, 4: 2024, 2: 2022, 1: 2021}, "air": {4: 2026, 3: 2025, 2: 2024, 1: 2022}}


def _special_model(n, core):
    """(семейство, год/поколение, линейка) для iPad, Apple Watch, AirPods, Galaxy Watch/Tab — или None."""
    year = re.search(r"\((20\d\d)\)", n)
    year = int(year.group(1)) if year else None
    if "ipad" in core:
        chip = re.search(r"\bm(\d)\b", core)
        if re.search(r"\bpro\b", core):
            line, tier = "pro", 4.0
        elif re.search(r"\bair\b", core):
            line, tier = "air", 3.0
        elif "mini" in core:
            line, tier = "mini", 0.5
        else:
            line, tier = "base", 1.0
        gen = year
        if gen is None and chip and line in _IPAD_CHIP_YEAR:
            gen = _IPAD_CHIP_YEAR[line].get(int(chip.group(1)))
        if gen is None and line == "base":
            m = re.search(r"ipad\s+(\d{1,2})\b", core)
            gen = {11: 2025, 10: 2022, 9: 2021}.get(int(m.group(1))) if m else None
        if gen is None and line == "mini":
            gen = 2024 if re.search(r"a17|\b7\b", core) else 2021
        size = re.search(r"\b(1[1-3])\b", core)
        return "apple ipad", gen or 0, tier + (int(size.group(1)) / 100 if size else 0)
    if "apple watch" in core:
        m = re.search(r"series\s*(\d+)", core)
        if m:
            return "apple watch", 2014 + int(m.group(1)), 3.0
        m = re.search(r"ultra\s*(\d*)", core)
        if m:
            return "apple watch", year or (2022 + int(m.group(1) or 1)), 5.0
        m = re.search(r"\bse\s*(\d*)", core)
        if m:
            return "apple watch", year or {"3": 2025, "2": 2022}.get(m.group(1), 2020), 1.0
        return "apple watch", year or 0, 2.0
    if "airpods" in core:
        line = "max" if "max" in core else "pro" if re.search(r"\bpro\b", core) else "base"
        m = re.search(r"airpods\s+(?:pro\s+|max\s+)?(\d)", core)
        return "airpods " + line, int(m.group(1)) if m else 1, 1.0
    m = re.search(r"galaxy watch\s*(\d+)", core)
    if m:
        return "samsung galaxy watch", 2016 + int(m.group(1)), 4.0 if "classic" in core else 3.0
    if "galaxy watch" in core:
        return "samsung galaxy watch", year or 2024, 5.0 if "ultra" in core else 2.0
    return None


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
    sp = _special_model(n, core)
    if sp:
        return sp[0], sp[1], sp[2], storage
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
    family = re.sub(r"wi-?fi|\blte\b|\b5g\b|\b4g\b|cellular|сотовая связь|\bgps\b|\besim\b|\bnfc\b|\+\s*клавиатура|клавиатура", " ", plain)
    family = re.sub(r"\d+e\b|\d+|pro\s*max|ultra|\bpro\b|\bair\b|\bplus\b|\bfe\b|\blite\b|\bmini\b|\+", " ", family)
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
