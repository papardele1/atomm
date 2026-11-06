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
            "Игры и приставки", "Техника для дома и красоты", "Камеры и дроны",
            "Конструкторы Lego", "Аксессуары"]

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
    (("Конструктор",), "Конструкторы Lego"),
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


# Не продаём: всё с маркой Store77, восстановленное, «Селект / как новое», уценку, их услуги и доработки.
EXCLUDED_SUBS = {"Store77 Outlet", "Восстановленная техника", "Техника Селект (как новая)", "Уцененная техника",
                 "Настройка компьютеров Mac", "Гравировка и клавиши"}
_EXCLUDED_NAME = re.compile(r"store\s*77|стор\s*77|восстановлен|\(селект|селект\)|уценк|как нов|"
                            r"создание учетной записи", re.I)


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
    goods.sort(key=lambda g: (SECTIONS.index(g["section"]), g["brand"] or "яя", g["sub"], -g["price"]))
    brands = sorted({g["brand"] for g in goods if g["brand"]})
    subs = sorted({g["sub"] for g in goods})
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
