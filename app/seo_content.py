"""Уникальные тексты для SEO-страниц моделей и статьи-гайды.

Правила наполнения:
- цвета, объёмы памяти, SIM-варианты и цены — только из каталога, подставляются динамически
  через плейсхолдеры ({colors}, {mems}, {sim}, {mem_links}, {lo} …), в статичный текст не вписываются;
- характеристики устройств (экран, чип, камеры, вес, автономность) — только проверенные
  по apple.com или крупным СМИ (источники — в SOURCES);
- условия магазина (гарантия, доставка) здесь не повторяются: они выводятся в блоке «О покупке…».

Тексты — доверенный HTML (пишем сами); значения плейсхолдеров экранирует seo.py.
"""

GUIDE_18PRO = "/guides/iphone-18-pro-vs-18-pro-max/"
GUIDE_17_18 = "/guides/iphone-17-pro-max-vs-18-pro-max/"
GUIDE_WHICH = "/guides/kakoy-iphone-kupit-2026/"
GUIDE_SIM = "/guides/iphone-18-pro-max-esim-ili-nano-sim/"
GUIDE_MEM = "/guides/iphone-18-pro-max-skolko-pamyati/"
GUIDE_MEM_PRO = "/guides/iphone-18-pro-skolko-pamyati/"
GUIDE_AIRPODS = "/guides/airpods-4-ili-airpods-5/"

SOURCES = {
    "iphone-18-pro": ["https://www.apple.com/iphone-18-pro/specs/", "https://www.apple.com/au/iphone-18-pro/specs/",
                      "https://engadget.com/2276013/iphone-18-pro-vs-max-comparison"],
    # iPhone 17 Pro: экран, чип, камеры, корпус, IP68, USB-C — ca/au; 204 г и 31 ч — версия с nano-SIM (au),
    # 206 г и 33 ч — версия только с eSIM (ca); разница по SIM подтверждена 9to5mac
    "iphone-17-pro": ["https://www.apple.com/uk/iphone-17-pro/specs", "https://www.apple.com/ca/iphone-17-pro/specs/",
                      "https://www.apple.com/au/iphone-17-pro/specs/",
                      "https://9to5mac.com/2025/09/10/iphone-17-pro-esim-best-battery-life/"],
    "iphone-17": ["https://appleinsider.com/articles/25/09/09/apples-base-iphone-17-grows-up-with-a-better-screen-improved-cameras"],
    "iphone-air": ["https://en.wikipedia.org/wiki/IPhone_Air", "https://www.techradar.com/phones/iphone/apple-iphone-air-review",
                   "https://macrumors.com/2025/09/09/iphone-17-a19-chip"],
    # S26 Ultra: экран, камеры, зарядка, S Pen в комплекте — samsung.com/us;
    # чип, вес, размеры, отличия от S25 Ultra — samsung.com/ie;
    # Privacy Display, S Pen, IP68 — samsung.com/uk; Gorilla Armor 2, 2600 нит — samsung.com/us compare, GSMArena
    "galaxy-s26-ultra": ["https://www.samsung.com/us/support/answer/ANS10010342/",
                         "https://www.samsung.com/ie/support/mobile-devices/what-are-the-differences-between-the-galaxy-s26-and-s25-series/",
                         "https://www.samsung.com/uk/smartphones/galaxy-s26-ultra/",
                         "https://www.samsung.com/us/smartphones/galaxy-s26-ultra/compare/",
                         "https://www.gsmarena.com/samsung_galaxy_s26_ultra-review-2939.php"],
    # 24 ч против 30 ч у Pro 2 (общий заряд с кейсом, данные Apple) — 9to5mac
    "airpods-pro-3": ["https://www.apple.com/airpods-pro/specs/",
                      "https://www.apple.com/newsroom/2025/09/introducing-airpods-pro-3-the-ultimate-audio-experience/",
                      "https://9to5mac.com/2025/09/10/airpods-pro-3-have-less-overall-battery-life-than-airpods-pro-2/"],
    # 17e: всё — apple.com/uk specs и newsroom; вес 170 г — UK (в США 169 г); отличия от 16e — newsroom и 9to5mac;
    # отсутствие ProMotion (60 Гц) — TechRadar
    "iphone-17e": ["https://www.apple.com/uk/iphone-17e/specs",
                   "https://www.apple.com/uk/newsroom/2026/03/apple-introduces-iphone-17e/",
                   "https://9to5mac.com/2026/03/02/iphone-17e-vs-iphone-16e/",
                   "https://www.techradar.com/phones/iphone/iphone-17e-vs-iphone-17"],
    "iphone-16-pro": ["https://support.apple.com/121031",
                      "https://www.apple.com/in/newsroom/2024/09/apple-debuts-iphone-16-pro-and-iphone-16-pro-max/"],
    "iphone-16-pro-max": ["https://support.apple.com/en-gb/121032"],
    # 17 Pro Max: 233 г / 39 ч — eSIM (US), 231 г / 37 ч — nano-SIM (IE); 18 Pro Max: 45 ч — CA (eSIM), 43 ч — UK (nano-SIM),
    # модем C2 — ca/148591; разница по SIM — ithinkdiff
    "iphone-17-18-pro-max": ["https://support.apple.com/125091", "https://support.apple.com/en-ie/125091",
                             "https://www.apple.com/uk/iphone-18-pro/specs/", "https://www.apple.com/ca/iphone-18-pro/specs/",
                             "https://support.apple.com/en-gb/148591",
                             "https://www.ithinkdiff.com/iphone-18-pro-battery-life-region/"],
    # iPhone 16: всё — support.apple.com/en-ie (версия с nano-SIM + eSIM; в US — только eSIM);
    # экран 60 Гц (ProMotion только у Pro) — SlashGear
    "iphone-16": ["https://support.apple.com/en-ie/121029", "https://support.apple.com/en-us/121029",
                  "https://www.slashgear.com/1667559/does-iphone-16-have-120hz-refresh-rate"],
    # iPhone 16 Plus: en-in — версия с nano-SIM (199 г, 27 ч, как и eSIM-версия в US)
    "iphone-16-plus": ["https://support.apple.com/en-in/121030", "https://support.apple.com/en-us/121030",
                       "https://www.slashgear.com/1667559/does-iphone-16-have-120hz-refresh-rate"],
    # iPhone 17: 177 г, 30 ч, 120 Гц — en-in (nano-SIM); iPhone Air: 165 г, 5,64 мм, 27 ч, только eSIM — en-us
    "iphone-17-specs": ["https://support.apple.com/en-in/125089"],
    "iphone-air-specs": ["https://support.apple.com/en-us/125092"],
    "apple-watch-ultra-3": ["https://support.apple.com/125095",
                            "https://9to5mac.com/2025/09/19/apple-watch-ultra-3-vs-ultra-2-heres-everything-new/"],
    # S25 Ultra: 6,9″, Snapdragon 8 Elite, 12 ГБ, камеры, 5000 мА·ч, 162,8×77,6×8,2 мм, 218 г, IP68, титан — samsung.com/nz;
    # QHD+ 3120×1440, 120 Гц, 2600 нит, Gorilla Armor 2, 45 Вт, S Pen без Bluetooth — GSMArena;
    # отличия от S26 Ultra — samsung.com/ie (как у S26 Ultra)
    "galaxy-s25-ultra": ["https://www.samsung.com/nz/smartphones/galaxy-s25-ultra/specs/",
                         "https://gsmarena.com/samsung_galaxy_s25_ultra-review-2793.php",
                         "https://www.samsung.com/ie/support/mobile-devices/what-are-the-differences-between-the-galaxy-s26-and-s25-series/"],
    # MacBook Pro 14″ M5 (2025): 10/10 ядер, до 32 ГБ, 3× Thunderbolt 4, до 24 ч видео, 1,55 кг — support 125405;
    # 14″ M5 Pro/Max (2026): экран, ядра, память, Thunderbolt 5, 22/20 ч, 1,60/1,62 кг — support en-gb/126318;
    # 16″ M5 Pro/Max: экран, 24/22 ч, 2,14/2,15 кг, порты, камера 12 Мп — apple.com/ae specs; дата (март 2026) — MacStories;
    # замена базовой модели на M6 (27.10.2026) — MacRumors, OLED-версия M5 Pro/Max (28.10.2026) — MacDailyNews
    "macbook-pro-m5": ["https://support.apple.com/125405", "https://support.apple.com/en-gb/126318",
                       "https://www.apple.com/ae/macbook-pro-14-and-16/specs/",
                       "https://www.macstories.net/?p=196276",
                       "https://macrumors.com/2026/10/27/14-inch-macbook-pro-with-m6-chip/",
                       "https://macdailynews.com/2026/10/28/apple-unveils-groundbreaking-macbook-pro-with-proled-xdr-display/"],
    # iPad Air 11″ M4: всё — support en-gb/126471; дата, +50% памяти, «до 30% быстрее M3», N1, C1X — UK newsroom
    "ipad-air-11-m4": ["https://support.apple.com/en-gb/126471",
                       "https://www.apple.com/uk/newsroom/2026/03/apple-introduces-the-new-ipad-air-powered-by-m4"],
    # подборки: MacBook Air M5 — newsroom; MacBook Neo — support 126322; iPad — apple.com/ipad/compare
    "macbook-air-m5": ["https://www.apple.com/newsroom/2026/03/apple-introduces-the-new-macbook-air-with-m5/"],
    "macbook-neo": ["https://support.apple.com/en-us/126322"],
    "ipad-compare": ["https://www.apple.com/ipad/compare/",
                     "https://www.apple.com/ipad/compare/?modelList=ipad-mini-a17pro%2Cipad-air-11-m3%2Cipad-11th-a16"],
    # SIM-версии iPhone 18 Pro / Pro Max: страны и номера моделей — support 108044; где смотреть номер — 106343;
    # eSIM-версия (US) и nano-SIM + eSIM (IE) — 148590/148591; Китай: nano-SIM или eSIM — 123879;
    # eSIM у МТС, Билайна, МегаФона и T2 дистанционно через Госуслуги — iPhones.ru (декабрь 2025)
    "iphone-18-sim": ["https://support.apple.com/en-us/108044", "https://support.apple.com/en-us/106343",
                      "https://support.apple.com/en-us/148591", "https://support.apple.com/en-ie/148591",
                      "https://support.apple.com/en-us/148590", "https://support.apple.com/en-ie/148590",
                      "https://support.apple.com/en-us/123879", "https://www.iphones.ru/iNotes/esim-2026-russia"],
    # подборки AirPods, Apple Watch: AirPods 5 — newsroom 2026/09; AirPods Max 2 — MacRumors 16.03.2026;
    # Apple Watch Ultra 4 (S11, «два дня» работы) — MacRumors 09.09.2026
    "airpods-5": ["https://www.apple.com/sg/newsroom/2026/09/apple-introduces-airpods-5-with-best-in-class-open-ear-active-noise-cancellation/",
                  "https://support.apple.com/en-us/148760"],
    "airpods-max-2": ["https://macrumors.com/2026/03/16/apple-announces-airpods-max-2/"],
    "apple-watch-ultra-4": ["https://macrumors.com/2026/09/09/apple-watch-ultra-4-announced-battery-life/"],
    "apple-watch-series-12": ["https://apple.com/newsroom/2026/09/introducing-apple-watch-series-12-with-the-all-new-health-sensing-system/"],
    "airpods-5-vs-wireless": ["https://macrumors.com/guide/airpods-5-vs-with-wireless-charging-case/"],
    # iPad Air 13″ M4: всё — support 126472; «до 30% быстрее M3» — UK newsroom (как у 11″ M4);
    # Magic Keyboard для iPad Air (14 функциональных клавиш, трекпад) — apple.com/ipad-keyboards
    "ipad-air-13-m4": ["https://support.apple.com/en-us/126472",
                       "https://www.apple.com/uk/newsroom/2026/03/apple-introduces-the-new-ipad-air-powered-by-m4",
                       "https://www.apple.com/ipad-keyboards/"],
    # iPad Air 11″ M3: всё — support 122241; «почти вдвое быстрее M1», трассировка лучей, Apple Intelligence,
    # новая Magic Keyboard, дата (март 2025) — newsroom 2025/03
    "ipad-air-11-m3": ["https://support.apple.com/en-us/122241",
                       "https://www.apple.com/newsroom/2025/03/apple-introduces-ipad-air-with-powerful-m3-chip-and-new-magic-keyboard/",
                       "https://www.apple.com/ipad-keyboards/"],
    # iPad (A16): всё — support 122240; Magic Keyboard Folio и Apple Pencil — apple.com/ipad-11 и ipad-keyboards
    "ipad-a16": ["https://support.apple.com/en-us/122240", "https://www.apple.com/ipad-11/",
                 "https://www.apple.com/ipad-keyboards/"],
    # iPad mini (A17 Pro): всё — support 121456; +30% CPU, +25% GPU, 2× Neural Engine, 128 ГБ вдвое больше,
    # USB-C вдвое быстрее, дата (23.10.2024) — newsroom 2024/10; клавиатуры Apple для mini нет — ipad-keyboards
    "ipad-mini-a17pro": ["https://support.apple.com/en-us/121456",
                         "https://www.apple.com/newsroom/2024/10/apple-introduces-powerful-new-ipad-mini-built-for-apple-intelligence/",
                         "https://www.apple.com/ipad-keyboards/"],
    # память iPhone 18 Pro Max: объёмы, 12–24 ГБ под систему, видеоформаты, USB 3 — support 148591;
    # ProRes до 30 раз больше HEVC, ограничения по объёму и внешней записи — support 109041;
    # iCloud Photos хранит оригиналы, оптимизация хранилища — support 108782
    "iphone-18-pro-max-memory": ["https://support.apple.com/en-us/148591", "https://support.apple.com/en-us/109041",
                                 "https://support.apple.com/en-us/108782"],
    # iPhone 15: экран, A16, камеры, видео, USB 2, 20 ч видео, размеры/вес, IP68, объёмы — support 111831;
    # нет Apple Intelligence (список устройств: iPhone 15 Pro/Pro Max, iPhone 16 и новее) — support 121115
    "iphone-15": ["https://support.apple.com/en-us/111831", "https://support.apple.com/en-us/121115"],
    # iPhone 16e: экран, A18 (4-ядерная графика), модем C1, камера 48 Мп, Action, Qi, USB 2, 26 ч, 167 г, IP68 — 122208
    "iphone-16e": ["https://support.apple.com/en-us/122208"],
    # iPad Pro M5: экран, нанотекстура (1/2 ТБ), CPU/RAM по объёму, вес/толщина, Thunderbolt/USB 4, N1, C1X, eSIM,
    # батарея — support 125407 (13″) и 125406 (11″)
    "ipad-pro-13-m5": ["https://support.apple.com/en-us/125407"],
    "ipad-pro-11-m5": ["https://support.apple.com/en-us/125406"],
    # Mac mini M6: ядра, память, порты, N1/Wi-Fi 7, Ethernet 2,5 Гбит/с, до трёх мониторов, размеры — apple.com/mac-mini/specs;
    # +40% CPU / 2× графика к M4, «на два ядра больше», продажи с 22.09.2026 — newsroom 2026/08; 2 нм — 9to5mac;
    # полоса памяти M6: 153 ГБ/с с 16 ГБ, 170 ГБ/с с 24/32 ГБ — apple.com/mac-mini/specs;
    # M4 / M4 Pro (Wi-Fi 6E, BT 5.3, гигабитный Ethernet, Thunderbolt 4/5, 273 ГБ/с) — support 121555
    "mac-mini-m6": ["https://www.apple.com/mac-mini/specs/",
                    "https://www.apple.com/newsroom/2026/08/apple-unveils-a-more-powerful-mac-mini-featuring-the-all-new-m6-and-m5-pro/",
                    "https://9to5mac.com/2026/08/25/apple-announces-new-mac-mini-heres-everything-new/",
                    "https://support.apple.com/en-us/121555"],
    # память iPhone 18 Pro: объёмы 256 ГБ–2 ТБ, 12–24 ГБ под систему (вкл. удаляемые приложения Apple ~4,5 ГБ),
    # ~7 ГБ — модели Apple Intelligence, 4K Dolby Vision 60 к/с на все камеры и 100/120 к/с на основную, ProRes до 4K 120 к/с
    # с внешней записью, ProRes RAW, Apple Log 2, USB 3 до 10 Гбит/с — support 148590; ProRes до 30× больше HEVC — 109041;
    # «Фото iCloud» и оптимизация хранилища — 108782
    "iphone-18-pro-memory": ["https://support.apple.com/en-us/148590", "https://support.apple.com/en-us/109041",
                             "https://support.apple.com/en-us/108782"],
    # AirPods 4 и AirPods 4 с шумоподавлением: H2, IP54, Bluetooth 5.3, 4,3 г, батарея (5 ч / 30 ч у обычных;
    # 4–5 ч / 20–30 ч у ANC), кейс USB-C 32,3 г или USB-C + Qi + зарядка Apple Watch с динамиком 34,7 г — apple.com/specs;
    # ANC-версия, 2024 год, динамик для «Локатора» — support 121204
    "airpods-4": ["https://www.apple.com/tj/airpods-4/specs/", "https://support.apple.com/en-mide/121204"],
    # AirPods 5: обе версии с ANC и H2; базовая — 4/6 ч, 20 ч с кейсом, кейс USB-C 32,3 г (support 148759);
    # с кейсом беспроводной зарядки — 5/7 ч, 22 ч, USB-C + Qi + зарядка Apple Watch, динамик («Локатор» с iOS 27),
    # регулировка громкости свайпом, кейс 34,7 г (support 148760); обе версии на одной странице — apple.com/sg specs;
    # «до 50% больше шума, чем AirPods 4 с ANC», «на час дольше», улучшенная защита от пыли/пота/воды, 18.09.2026 —
    # newsroom; IP57 — и в таблице, и в сноске на apple.com/au specs и support en-au/148759 (в sg/uk сноска IP54 —
    # расхождение на этих страницах, ориентируемся на au)
    "airpods-5-specs": ["https://support.apple.com/en-gb/148759", "https://support.apple.com/en-gb/148760",
                        "https://www.apple.com/au/airpods-5/specs/", "https://support.apple.com/en-au/148759",
                        "https://www.apple.com/sg/airpods-5/specs",
                        "https://www.apple.com/sg/newsroom/2026/09/apple-introduces-airpods-5-with-best-in-class-open-ear-active-noise-cancellation/"],
    # Series 12: размеры, материалы и цвета, экран 2000 нит, S11 64 ГБ, 24/38 ч, 10 ч тренировки, 80% за ~30 мин,
    # 50 м, IP6X, датчики, вес, совместимость iPhone 11+ с iOS 27 — apple.com specs;
    # Health Sensing System, пульс каждые 5 с, HRV до 24 раз чаще, +25% тренировка, +50% к 15-минутной зарядке,
    # Ceramic Shield 2 на 60% прочнее Ion-X у Series 11, керамика — новинка, 18.09.2026 — newsroom
    "apple-watch-series-12-specs": ["https://www.apple.com/apple-watch-series-12/specs/",
                                    "https://apple.com/newsroom/2026/09/introducing-apple-watch-series-12-with-the-all-new-health-sensing-system/"],
    # Ultra 4: титан Grade 5, 49 мм, 63 г, экран 3000 нит, 422×514, 1245 мм², S11, 50/84 ч, тренировка 18/25/45 ч,
    # 80% за ~45 мин, 100 м, дайвинг до 40 м, IP6X, MIL-STD 810H, двухчастотный GPS, iPhone 11+ с iOS 27 — apple.com specs;
    # «два дня», 18.09.2026 — MacRumors; новые оптический и электрический датчики, пульс каждые 5 с — newsroom;
    # Ultra 3 (42/72 ч, S10) — support 125095
    "apple-watch-ultra-4-specs": ["https://www.apple.com/apple-watch-ultra-4/specs/",
                                  "https://macrumors.com/2026/09/09/apple-watch-ultra-4-announced-battery-life/",
                                  "https://apple.com/newsroom/2026/09/apple-unveils-apple-watch-ultra-4",
                                  "https://support.apple.com/125095"],
    # Galaxy S26 и S26+: экраны (6,3″ FHD+ / 6,7″ QHD+), 120 Гц, Exynos 2600 / Snapdragon 8 Elite Gen 5 по рынкам, 12 ГБ,
    # 4300 / 4900 мА·ч, размеры и вес (167 / 190 г), камеры 50+12+10 Мп (3×), фронтальная 12 Мп, IP68 — newsroom;
    # 2600 нит, Gorilla Glass Victus 2, Armor Aluminum, до 30 / 31 ч видео — samsung.com/au compare;
    # 25 / 45 Вт по проводу, 15 / 20 Вт без проводов, Snapdragon — Северная Америка, Китай, Япония — SamMobile, GSMArena
    "galaxy-s26": ["https://news.samsung.com/global/samsung-unveils-galaxy-s26-series-the-most-intuitive-galaxy-ai-phone",
                   "https://www.samsung.com/au/smartphones/galaxy-s26/compare/",
                   "https://www.gsmarena.com/galaxy_s26_debuts_with_larger_63_screen_and_4300mah_battery_s26_also_launches-news-71699.php"],
    "galaxy-s26-plus": ["https://news.samsung.com/global/samsung-unveils-galaxy-s26-series-the-most-intuitive-galaxy-ai-phone",
                        "https://www.samsung.com/au/smartphones/galaxy-s26/compare/",
                        "https://www.sammobile.com/news/samsung-galaxy-s26-plus-vs-s26-key-differences/"],
    # Z Fold8 (широкий формат) и Z Flip8: экраны, размеры, вес, чип, память, камеры, батарея, зарядка, IP48, дата
    # (22.07.2026) — UK newsroom; соотношение сторон 4:3 / 10:16, 45 Вт, отличия от Fold8 Ultra, нет S Pen — Android Central;
    # Flip8: Exynos 2600 / Snapdragon по рынкам, 25 Вт / 15 Вт, отличия от Flip7 (6,5 мм, 188 г) — Android Authority
    "galaxy-z-fold8": ["https://news.samsung.com/uk/samsung-galaxy-z-fold8-ultra-fold8-and-flip8-foldables-perfected-for-every-way-of-living",
                       "https://www.androidcentral.com/phones/samsung-galaxy/samsung-galaxy-z-fold-8-ultra-vs-galaxy-z-fold-8"],
    "galaxy-z-flip8": ["https://news.samsung.com/uk/samsung-galaxy-z-fold8-ultra-fold8-and-flip8-foldables-perfected-for-every-way-of-living",
                       "https://www.androidauthority.com/samsung-galaxy-z-flip-8-3687727/"],
    # MacBook Air M5: чип, память, SSD, экран, батарея (Вт·ч, 18 / 15 ч), вес, толщина, порты, мониторы, камера, динамики,
    # N1 / Wi-Fi 7 / Bluetooth 6, цвета — support 126320 (13″) и 126321 (15″)
    "macbook-air-m5-13": ["https://support.apple.com/en-us/126320"],
    "macbook-air-m5-15": ["https://support.apple.com/en-us/126321"],
}
# статья «AirPods 4 или AirPods 5»
SOURCES["airpods-4-vs-5"] = SOURCES["airpods-4"] + SOURCES["airpods-5-specs"]

# Абзац = список фрагментов (HTML). Фрагмент выпадает, если хоть один его плейсхолдер пуст
# (нет наличия, нет цветов/памяти, нет страницы модели); пустой абзац не выводится.
# FAQ = (вопрос, [фрагменты ответа]); если выпал первый (основной) фрагмент — вопрос не выводится.
# Плейсхолдеры (seo.variants_ctx): {colors} {mems} {sim} {mem_links} — только по товарам в наличии;
# {sim_answer} — прямой ответ «Да/Нет» про физическую SIM;
# {link_<slug с _ вместо ->} — ссылка на страницу модели, если она есть в каталоге;
# {guide} — ссылка на статью «18 Pro или 18 Pro Max», {guide_17_18} — «17 Pro Max или 18 Pro Max»,
# {guide_airpods} — «AirPods 4 или AirPods 5».
MODELS = {
    "apple-iphone-18-pro-max": {
        "h2": "Что важно знать об iPhone 18 Pro Max",
        "paras": [
            ["Старшая Pro-модель с OLED-экраном 6,9 дюйма (2868×1320 точек, 460 ppi), ProMotion до 120 Гц "
             "и яркостью до 3000 нит на улице. Внутри — чип A20 Pro, такой же, как у младшей Pro-модели. "
             "Сзади три камеры по 48 Мп: основная с переменной диафрагмой ƒ/1.48–ƒ/4.0, сверхширокоугольная "
             "и телефото с 4-кратным приближением. Фронтальная камера — 18 Мп с Center Stage."],
            ["Главный довод в пользу Pro Max — автономность. По данным Apple, версия только с eSIM выдерживает "
             "до 45 часов воспроизведения видео, версия с лотком для nano-SIM — до 43 часов. Плата за это — "
             "габариты 163,4×78,0×8,75 мм и вес 249 г. Корпус алюминиевый, защита от воды и пыли по IP68, "
             "разъём USB-C со скоростью USB 3 до 10 Гбит/с."],
            ["В ATOMM смартфон есть в цветах: {colors}.", "Объём памяти — {mems}.", "{sim}",
             "Сомневаетесь, нужен ли такой размер? Сравнили обе модели в статье {guide}.",
             "Варианты по памяти: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета iPhone 18 Pro Max есть в наличии?",
             ["Сейчас в наличии: {colors}.",
              "Наличие по цветам меняется в течение дня — актуальные варианты в списке товаров на этой странице."]),
            ("eSIM или Nano SIM + eSIM — что выбрать?",
             ["В версии только с eSIM нет лотка для SIM-карты: номер подключается как электронная SIM, одновременно "
              "работают две eSIM. Версия Nano SIM + eSIM позволяет вставить обычную SIM-карту и добавить вторую линию "
              "на eSIM. По данным Apple, eSIM-версия работает чуть дольше: до 45 часов видео против 43 часов. "
              "Перед покупкой eSIM-версии уточните у своего оператора, выдаёт ли он eSIM.",
              "Как отличить версии по номеру модели и какая продаётся в разных странах — в статье {guide_sim}."]),
            ("Чем 18 Pro отличается от 18 Pro Max?",
             ["Pro Max выбирают ради экрана и батареи: 6,9 дюйма вместо 6,3 и до 45 часов видео против 36 у 18 Pro "
              "(версии только с eSIM). Расплата — вес 249 г против 211 г. Чип A20 Pro, камеры, объёмы памяти и цвета "
              "у моделей одинаковые.",
              "Подробное сравнение — в статье {guide}."]),
            ("Чем iPhone 18 Pro Max отличается от 17 Pro Max?",
             ["Размер экрана не изменился — 6,9 дюйма. Новинка получила чип A20 Pro (у 17 Pro Max — A19 Pro) "
              "и работает дольше: в версиях с nano-SIM Apple обещает до 43 часов видео, у 17 Pro Max — до 37. "
              "Взамен 18 Pro Max стал тяжелее: 249 г против 231 г.",
              "Все отличия — в статье {guide_17_18}."]),
            ("Сколько памяти выбрать в iPhone 18 Pro Max?",
             ["Сейчас в наличии: {mems}. Память в iPhone не расширяется картой, поэтому объём лучше выбирать с запасом: "
              "самого младшего объёма линейки хватает при обычной съёмке и хранении архива в iCloud, а большие объёмы нужны тем, кто много "
              "снимает в 4K и ProRes.",
              "Кому какой объём подойдёт — в статье {guide_mem}."]),
        ],
    },
    "apple-iphone-18-pro": {
        "h2": "Коротко об iPhone 18 Pro",
        "paras": [
            ["Компактная версия флагмана: экран 6,3 дюйма (2622×1206 точек, 460 ppi), ProMotion до 120 Гц, "
             "до 3000 нит на солнце. Чип A20 Pro и камеры те же, что у старшей модели: три модуля по 48 Мп — "
             "основной с переменной диафрагмой, сверхширокоугольный и 4-кратный телефото, плюс фронтальная "
             "камера 18 Мп."],
            ["Размеры — 150,0×71,9×8,75 мм, вес 211 г: телефон на 38 г легче Pro Max, и им удобнее пользоваться "
             "одной рукой. Время работы, по данным Apple, — до 36 часов видео у версии только с eSIM и до 34 часов "
             "у версии с nano-SIM. Корпус из алюминия, защита IP68, USB-C со скоростью USB 3 до 10 Гбит/с."],
            ["Сейчас в ATOMM доступны цвета: {colors}.", "Память — {mems}.", "{sim}",
             "Если выбираете между размерами, загляните в наше сравнение — {guide}.",
             "Отдельные страницы по объёму: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета iPhone 18 Pro есть в наличии?",
             ["В наличии: {colors}.", "Список обновляется вместе с каталогом несколько раз в день."]),
            ("Что лучше: eSIM или Nano SIM + eSIM?",
             ["Версия только с eSIM не имеет лотка для SIM-карты, зато, по данным Apple, дольше работает — до 36 часов "
              "видео против 34 часов у версии с nano-SIM. Если вы пользуетесь обычной SIM-картой и не хотите переходить "
              "на eSIM, выбирайте Nano SIM + eSIM. Какая версия перед вами, указано в названии каждого товара.",
              "Подробнее о версиях для разных стран — в статье {guide_sim}."]),
            ("Чем 18 Pro отличается от 18 Pro Max?",
             ["18 Pro — тот же флагман в меньшем корпусе: камеры, чип A20 Pro, память и цвета не урезаны. "
              "Он легче (211 г против 249 г) и с экраном 6,3 дюйма вместо 6,9, но батареи хватает на меньшее время: "
              "до 36 часов видео против 45 у Pro Max в версиях только с eSIM.",
              "Разбираем выбор в статье {guide}."]),
            ("Сколько памяти выбрать в iPhone 18 Pro?",
             ["Сейчас в наличии: {mems}. Карту памяти в iPhone не вставить, поэтому объём выбирают с расчётом на несколько "
              "лет: базового хватает для обычной съёмки с архивом в облаке, а старшие версии нужны тем, кто снимает много "
              "видео в 4K или в ProRes.",
              "Подробный разбор — в статье {guide_mem_pro}."]),
        ],
    },
    "apple-iphone-17-pro-max": {
        "h2": "iPhone 17 Pro Max: что внутри",
        "paras": [
            ["Флагман прошлого поколения с экраном 6,9 дюйма и чипом A19 Pro. Корпус — алюминиевый unibody "
             "с Ceramic Shield 2 спереди. Сзади три камеры по 48 Мп: основная (24 мм), сверхширокоугольная (13 мм) "
             "и телефото 100 мм с 4-кратным приближением; фронтальная — 18 Мп с Center Stage. По данным Apple, "
             "версия Nano SIM + eSIM весит 231 г и воспроизводит видео до 37 часов, версия только с eSIM — 233 г "
             "и до 39 часов."],
            ["Модель остаётся разумной альтернативой 18 Pro Max: размер экрана тот же, а разница — в более новом "
             "чипе A20 Pro, более высокой автономности и в большем весе новинки. Если эти отличия для вас "
             "не принципиальны, 17 Pro Max — по-прежнему актуальный выбор."],
            ["В ATOMM доступны цвета: {colors}.", "Объём памяти — {mems}.", "{sim}",
             "Выбрать по памяти: {mem_links}.", "Для сравнения — {link_apple_iphone_18_pro_max}.",
             "Чем модели отличаются и стоит ли переплачивать за новинку, разобрали в статье {guide_17_18}."],
        ],
        "faq": [
            ("Какие цвета iPhone 17 Pro Max есть в наличии?",
             ["В наличии: {colors}."]),
            ("Есть ли iPhone 17 Pro Max с физической SIM-картой?",
             ["{sim_answer}"]),
            ("Чем iPhone 17 Pro Max отличается от 18 Pro Max?",
             ["Обе модели с экраном 6,9 дюйма. 17 Pro Max легче — 231 г против 249 г, но работает на чипе предыдущего "
              "поколения (A19 Pro против A20 Pro) и меньше держит заряд: до 37 часов видео против 43 у 18 Pro Max, "
              "если сравнивать версии с nano-SIM.",
              "Подробнее — в статье {guide_17_18}."]),
        ],
    },
    "apple-iphone-17": {
        "h2": "Коротко об iPhone 17",
        "paras": [
            ["Базовый iPhone 2025 года получил экран 6,3 дюйма с ProMotion до 120 Гц и яркостью до 3000 нит на улице. "
             "Внутри — чип A19. Сзади две камеры по 48 Мп: основная и сверхширокоугольная, спереди — 18 Мп "
             "с Center Stage и квадратным сенсором. Память начинается с 256 ГБ."],
            ["От iPhone 17 Pro модель отличается чипом (A19 против A19 Pro) и отсутствием телефото-камеры "
             "с 4-кратным приближением. Если снимаете в основном на основную и сверхширокоугольную камеры, "
             "базовой модели хватит для большинства сценариев. Сверхширокоугольная камера теперь тоже 48 Мп, "
             "поэтому кадры с неё детальнее, чем у предыдущих базовых iPhone. Время работы, по данным Apple, — "
             "до 30 часов воспроизведения видео."],
            ["В ATOMM iPhone 17 есть в цветах: {colors}.", "Объём памяти — {mems}.", "{sim}",
             "Страницы по памяти: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета iPhone 17 есть в наличии?",
             ["В наличии: {colors}."]),
            ("eSIM или Nano SIM + eSIM — в чём разница?",
             ["В версии только с eSIM нет лотка для SIM-карты, номер подключается как электронная SIM. Версия Nano SIM + eSIM "
              "принимает обычную SIM-карту и eSIM одновременно.", "{sim}"]),
            ("Чем iPhone 17 отличается от iPhone 17 Pro?",
             ["У 17 Pro чип A19 Pro и третья камера — телефото 48 Мп с 4-кратным приближением. У iPhone 17 — чип A19 "
              "и две камеры по 48 Мп: основная и сверхширокоугольная. Экран у обеих моделей 6,3 дюйма."]),
        ],
    },
    "apple-iphone-air": {
        "h2": "Что нужно знать об iPhone Air",
        "paras": [
            ["Самый тонкий из нескладных iPhone: толщина корпуса — 5,64 мм, вес — 165 г. Рамка из титана, "
             "спереди стекло Ceramic Shield 2, сзади — Ceramic Shield, защита по IP68. Экран 6,5 дюйма с ProMotion "
             "до 120 Гц. Чип — A19 Pro, как у iPhone 17 Pro, но с 5-ядерным графическим процессором вместо 6-ядерного."],
            ["Компромиссы ради толщины: сзади одна камера 48 Мп без сверхширокоугольного модуля и телефото, "
             "а батарея скромнее, чем у Pro-моделей. Фронтальная камера — 18 Мп с Center Stage. "
             "Физической SIM-карты нет: iPhone Air работает только с eSIM во всех странах. "
             "Модель подойдёт тем, кому важнее лёгкий и тонкий корпус, чем несколько камер и максимальная автономность.",
             "Если нужны телефото-модуль и больший запас батареи, посмотрите в сторону {link_apple_iphone_17_pro}."],
            ["В ATOMM доступны цвета: {colors}.", "Объём памяти — {mems}.",
             "Перед покупкой уточните у своего оператора, выдаёт ли он eSIM.", "Варианты по памяти: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета iPhone Air есть в наличии?",
             ["В наличии: {colors}."]),
            ("Можно ли вставить обычную SIM-карту в iPhone Air?",
             ["Нет. Лотка для SIM-карты у iPhone Air нет ни в одной версии — только eSIM. Номер нужно перевести на eSIM "
              "у своего оператора."]),
            ("Чем iPhone Air отличается от iPhone 17 Pro?",
             ["Чип в обоих — A19 Pro, но у Air 5-ядерный графический процессор, а у 17 Pro — 6-ядерный. Air тоньше "
              "и легче (5,64 мм и 165 г против 204 г у 17 Pro), у него экран 6,5 дюйма против 6,3, но одна камера "
              "48 Мп вместо трёх."]),
        ],
    },
    "apple-iphone-17-pro": {
        "h2": "iPhone 17 Pro: главное о модели",
        "paras": [
            ["Pro-модель 2025 года с экраном 6,3 дюйма (2622×1206 точек, 460 ppi), ProMotion до 120 Гц и яркостью "
             "до 3000 нит на улице. Внутри — чип A19 Pro с 6-ядерным графическим процессором. Все три задние камеры — "
             "48-мегапиксельные: широкоугольная 24 мм, сверхширокоугольная 13 мм и телекамера 100 мм, которая даёт "
             "4-кратное приближение, а в режиме 8× — 12-мегапиксельные снимки оптического качества. Спереди — "
             "18-мегапиксельная камера с Center Stage."],
            ["Корпус — алюминиевый unibody, спереди Ceramic Shield 2, сзади Ceramic Shield. Защита IP68 рассчитана "
             "на погружение до 6 м на 30 минут, разъём USB-C работает со скоростью USB 3 до 10 Гбит/с. Вес и автономность "
             "зависят от версии: по данным Apple, модель с лотком для nano-SIM весит 204 г и воспроизводит видео "
             "до 31 часа, модель только с eSIM — 206 г и до 33 часов.",
             "Если нужен экран побольше и запас батареи, посмотрите {link_apple_iphone_17_pro_max}.",
             "Новое поколение в том же размере — {link_apple_iphone_18_pro}."],
            ["В ATOMM доступны цвета: {colors}.", "Объём памяти — {mems}.", "{sim}",
             "Выбрать по памяти: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета iPhone 17 Pro есть в наличии?",
             ["В наличии: {colors}."]),
            ("Есть ли iPhone 17 Pro с физической SIM-картой?",
             ["{sim_answer}"]),
            ("Чем iPhone 17 Pro отличается от 17 Pro Max?",
             ["Чип A19 Pro и камеры у моделей одинаковые. Младшая модель компактнее и легче: экран 6,3 дюйма вместо 6,9 "
              "и вес 204 г против 231 г, если сравнивать версии с nano-SIM. Зато Pro Max дольше работает: до 37 часов "
              "видео против 31 часа."]),
            ("Чем эта модель отличается от iPhone 18 Pro?",
             ["Экран у обеих моделей 6,3 дюйма. 18 Pro работает на чипе A20 Pro и дольше держит заряд — до 34 часов видео "
              "против 31 часа в версиях с nano-SIM, но весит больше: 211 г против 204 г."]),
        ],
    },
    "apple-iphone-17e": {
        "h2": "Коротко об iPhone 17e",
        "paras": [
            ["Самый доступный iPhone 2026 года: Apple представила его в марте. Экран OLED 6,1 дюйма (2532×1170 точек, "
             "460 ppi) с яркостью до 1200 нит в HDR, спереди стекло Ceramic Shield 2. Внутри — чип A19, как у iPhone 17, "
             "и собственный модем Apple C1X. Сзади одна камера 48 Мп Fusion: она снимает и с 2-кратным приближением "
             "оптического качества. Фронтальная камера — 12 Мп."],
            ["Размеры — 146,7×71,5×7,8 мм, вес около 170 г. По данным Apple, заряда хватает до 26 часов воспроизведения "
             "видео. Есть кнопка Action, беспроводная зарядка MagSafe и Qi2 до 15 Вт, защита IP68. Разъём USB-C работает "
             "на скорости USB 2.",
             "Если нужны экран побольше с ProMotion и вторая, сверхширокоугольная камера, посмотрите {link_apple_iphone_17}."],
            ["В ATOMM iPhone 17e есть в цветах: {colors}.", "Объём памяти — {mems}.", "{sim}",
             "Страницы по памяти: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета iPhone 17e есть в наличии?",
             ["В наличии: {colors}."]),
            ("Есть ли iPhone 17e с физической SIM-картой?",
             ["{sim_answer}"]),
            ("Чем iPhone 17e отличается от iPhone 16e?",
             ["Новая модель получила чип A19 вместо A18 и модем C1X вместо C1, а также поддержку MagSafe и Qi2 "
              "до 15 Вт — у 16e была только зарядка Qi до 7,5 Вт. Минимальный объём памяти вырос со 128 до 256 ГБ. "
              "Экран 6,1 дюйма и время работы до 26 часов видео остались прежними."]),
            ("Чем iPhone 17e отличается от iPhone 17?",
             ["У iPhone 17 экран больше — 6,3 дюйма — и с ProMotion до 120 Гц, сзади две камеры по 48 Мп "
              "(основная и сверхширокоугольная), фронтальная — 18 Мп, есть кнопка Camera Control, а видео он "
              "воспроизводит до 30 часов. У 17e — экран 6,1 дюйма, одна камера 48 Мп, фронтальная 12 Мп "
              "и до 26 часов видео, зато он дешевле."]),
        ],
    },
    "apple-iphone-16-pro": {
        "h2": "iPhone 16 Pro: что нужно знать",
        "paras": [
            ["Pro-модель 2024 года с экраном 6,3 дюйма (2622×1206 точек, 460 ppi), ProMotion до 120 Гц и яркостью "
             "до 2000 нит на улице. Корпус титановый, защита IP68. Внутри — чип A18 Pro. Сзади три камеры: "
             "основная 48 Мп Fusion, сверхширокоугольная 48 Мп и телефото 12 Мп с 5-кратным оптическим приближением; "
             "фронтальная — 12 Мп. Есть кнопки Camera Control и Action."],
            ["Размеры — 149,6×71,5×8,25 мм, вес 199 г. По данным Apple, заряда хватает до 27 часов воспроизведения видео. "
             "Разъём USB-C работает со скоростью USB 3 до 10 Гбит/с — удобно, если переносите на компьютер "
             "длинные ролики.",
             "Новее и с более ёмкой батареей — {link_apple_iphone_17_pro}."],
            ["В ATOMM доступны цвета: {colors}.", "Объём памяти — {mems}.", "{sim}",
             "Выбрать по памяти: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета iPhone 16 Pro есть в наличии?",
             ["В наличии: {colors}."]),
            ("Есть ли iPhone 16 Pro с физической SIM-картой?",
             ["{sim_answer}"]),
            ("Чем iPhone 16 Pro отличается от iPhone 17 Pro?",
             ["У 17 Pro чип A19 Pro, алюминиевый корпус вместо титанового, телефото 48 Мп с 4-кратным приближением "
              "вместо 12 Мп с 5-кратным и фронтальная камера 18 Мп вместо 12 Мп. Он дольше работает — до 31 часа видео "
              "против 27 часов (версии с nano-SIM), но весит больше: 204 г против 199 г. Экран у обеих моделей 6,3 дюйма."]),
        ],
    },
    "apple-iphone-16-pro-max": {
        "h2": "iPhone 16 Pro Max: главное о модели",
        "paras": [
            ["Старшая модель 2024 года с экраном 6,9 дюйма (2868×1320 точек, 460 ppi), ProMotion до 120 Гц и яркостью "
             "до 2000 нит на улице. Титановый корпус, защита IP68, чип A18 Pro. Камеры — как у 16 Pro: основная 48 Мп "
             "Fusion, сверхширокоугольная 48 Мп и телефото 12 Мп с 5-кратным оптическим приближением, цифровой зум — "
             "до 25×. Фронтальная камера — 12 Мп."],
            ["Размеры — 163×77,6×8,25 мм, вес 227 г. По данным Apple, заряда хватает до 33 часов воспроизведения видео. "
             "Разъём USB-C со скоростью USB 3 до 10 Гбит/с, есть кнопки Camera Control и Action.",
             "Следующие поколения — {link_apple_iphone_17_pro_max} и {link_apple_iphone_18_pro_max}."],
            ["В ATOMM доступны цвета: {colors}.", "Объём памяти — {mems}.", "{sim}",
             "Выбрать по памяти: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета iPhone 16 Pro Max есть в наличии?",
             ["В наличии: {colors}."]),
            ("Есть ли iPhone 16 Pro Max с физической SIM-картой?",
             ["{sim_answer}"]),
            ("Чем iPhone 16 Pro Max отличается от 17 Pro Max?",
             ["Экран у обеих моделей 6,9 дюйма. У 17 Pro Max чип A19 Pro, алюминиевый корпус вместо титанового, "
              "телефото 48 Мп с 4-кратным приближением вместо 12 Мп с 5-кратным и фронтальная камера 18 Мп. "
              "Он дольше работает — до 37 часов видео против 33 (версии с nano-SIM) — и чуть тяжелее: 231 г против 227 г."]),
        ],
    },
    "apple-iphone-16": {
        "h2": "iPhone 16: что важно знать",
        "paras": [
            ["Базовый iPhone 2024 года с OLED-экраном 6,1 дюйма (2556×1179 точек, 460 ppi): яркость до 1600 нит в HDR "
             "и до 2000 нит на улице. Внутри — чип A18. Сзади две камеры: основная 48 Мп Fusion (снимает "
             "и с 2-кратным приближением оптического качества) и сверхширокоугольная 12 Мп; фронтальная — 12 Мп. "
             "Есть кнопки Action и Camera Control."],
            ["Корпус алюминиевый, спереди Ceramic Shield, защита IP68 — до 6 м на 30 минут. Размеры — 147,6×71,6×7,8 мм, "
             "вес 170 г. По данным Apple, заряда хватает до 22 часов воспроизведения видео. Беспроводная зарядка MagSafe — "
             "до 25 Вт, разъём USB-C работает на скорости USB 2. Экран обновляется с частотой 60 Гц, без ProMotion.",
             "Плавный экран до 120 Гц и больше времени работы — у {link_apple_iphone_17}.",
             "Тот же чип и камеры с экраном 6,7 дюйма — {link_apple_iphone_16_plus}."],
            ["В ATOMM iPhone 16 есть в цветах: {colors}.", "Объём памяти — {mems}.", "{sim}",
             "Страницы по памяти: {mem_links}.",
             "Чем он отличается от других моделей, разобрали в статье {guide_which}."],
        ],
        "faq": [
            ("Какие цвета iPhone 16 есть в наличии?",
             ["В наличии: {colors}."]),
            ("Есть ли iPhone 16 с физической SIM-картой?",
             ["{sim_answer}"]),
            ("Чем iPhone 16 отличается от iPhone 17?",
             ["У iPhone 17 экран больше — 6,3 дюйма против 6,1 — и с ProMotion до 120 Гц вместо 60 Гц, чип A19 вместо A18, "
              "сверхширокоугольная камера 48 Мп вместо 12 Мп и фронтальная 18 Мп вместо 12 Мп. Видео он воспроизводит "
              "до 30 часов против 22. Память у iPhone 17 начинается с 256 ГБ, у iPhone 16 — со 128 ГБ."]),
            ("Чем iPhone 16 отличается от 16 Plus?",
             ["Чип A18, камеры, кнопки и материалы корпуса у моделей одинаковые. У 16 Plus экран 6,7 дюйма вместо 6,1, "
              "он тяжелее (199 г против 170 г) и дольше работает: до 27 часов видео против 22."]),
        ],
    },
    "apple-iphone-16-plus": {
        "h2": "Коротко об iPhone 16 Plus",
        "paras": [
            ["Версия базового iPhone 2024 года с большим экраном: OLED 6,7 дюйма (2796×1290 точек, 460 ppi), до 1600 нит "
             "в HDR и до 2000 нит на улице. Чип A18 и камеры — как у iPhone 16: основная 48 Мп Fusion с 2-кратным "
             "приближением оптического качества, сверхширокоугольная 12 Мп с углом обзора 120° и фронтальная 12 Мп. "
             "Есть кнопки Action и Camera Control."],
            ["Размеры — 160,9×77,8×7,8 мм, вес 199 г: при почти такой же диагонали, как у Pro Max, телефон заметно легче — "
             "16 Pro Max с экраном 6,9 дюйма весит 227 г. По данным Apple, 16 Plus воспроизводит видео до 27 часов. "
             "Корпус алюминиевый, Ceramic Shield спереди, защита IP68, MagSafe до 25 Вт, USB-C со скоростью USB 2. "
             "Частота обновления экрана — 60 Гц.",
             "Если нужны ProMotion и телефото с 5-кратным приближением, посмотрите {link_apple_iphone_16_pro_max}."],
            ["В ATOMM доступны цвета: {colors}.", "Объём памяти — {mems}.", "{sim}",
             "Выбрать по памяти: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета iPhone 16 Plus есть в наличии?",
             ["В наличии: {colors}."]),
            ("Есть ли iPhone 16 Plus с физической SIM-картой?",
             ["{sim_answer}"]),
            ("Что выбрать: iPhone 16 Plus или 16 Pro Max?",
             ["Обе модели 2024 года — с большим экраном. У 16 Pro Max экран 6,9 дюйма с ProMotion до 120 Гц, чип A18 Pro, "
              "титановый корпус, третья камера — телефото 12 Мп с 5-кратным приближением — и до 33 часов видео. "
              "16 Plus проще: 6,7 дюйма и 60 Гц, чип A18, две камеры и до 27 часов видео, зато он легче — 199 г против 227 г."]),
        ],
    },
    "samsung-galaxy-s26-ultra": {
        "h2": "Что нужно знать о Galaxy S26 Ultra",
        "paras": [
            ["Флагман Samsung 2026 года с экраном Dynamic AMOLED 2X 6,9 дюйма: разрешение QHD+, частота до 120 Гц, "
             "яркость до 2600 нит. Новинка этого поколения — встроенный режим Privacy Display. Он защищает экран "
             "от посторонних взглядов: можно скрыть весь экран или только выбранные приложения, уведомления и ввод "
             "PIN-кода или пароля. Перо S Pen хранится в корпусе. Работает смартфон на Snapdragon 8 Elite Gen 5 "
             "for Galaxy."],
            ["Сзади четыре камеры: основная 200 Мп (ƒ/1.4), сверхширокоугольная 50 Мп и два телефото — 10 Мп с 3-кратным "
             "и 50 Мп с 5-кратным оптическим приближением; цифровой зум — до 100×. Фронтальная камера — 12 Мп. "
             "Аккумулятор на 5000 мА·ч заряжается по проводу мощностью до 60 Вт и без проводов — до 25 Вт. "
             "Размеры — 163,6×78,1×7,9 мм, вес 214 г, спереди стекло Corning Gorilla Armor 2, защита от воды и пыли — IP68.",
             "Для сравнения — предыдущая модель {link_samsung_galaxy_s25_ultra}."],
            ["В ATOMM смартфон есть в цветах: {colors}.", "Встроенная память — {mems}.",
             "Страницы по объёму: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета Galaxy S26 Ultra есть в наличии?",
             ["Сейчас в наличии: {colors}."]),
            ("Чем S26 Ultra отличается от S25 Ultra?",
             ["Экран и аккумулятор прежние: 6,9 дюйма QHD+ и 5000 мА·ч. Новинка получила Snapdragon 8 Elite Gen 5 "
              "for Galaxy вместо Snapdragon 8 Elite for Galaxy, более светосильную основную камеру (ƒ/1.4 против ƒ/1.7), "
              "зарядку до 60 Вт вместо 45 Вт и режим Privacy Display. Корпус стал тоньше и легче: 7,9 мм и 214 г "
              "против 8,2 мм и 218 г."]),
            ("Есть ли в комплекте перо S Pen?",
             ["Да, S Pen встроен в корпус смартфона и входит в комплект."]),
        ],
    },
    "samsung-galaxy-s25-ultra": {
        "h2": "Galaxy S25 Ultra: главное о модели",
        "paras": [
            ["Флагман Samsung 2025 года с экраном Dynamic AMOLED 2X 6,9 дюйма: разрешение QHD+ (3120×1440), частота "
             "до 120 Гц, яркость до 2600 нит. Спереди — стекло Corning Gorilla Armor 2, рамка из титана, защита от воды "
             "и пыли по IP68. Работает смартфон на Snapdragon 8 Elite for Galaxy, оперативной памяти — 12 ГБ. "
             "Перо S Pen хранится в корпусе."],
            ["Сзади четыре камеры: основная 200 Мп (ƒ/1.7), сверхширокоугольная 50 Мп и два телефото — 10 Мп с 3-кратным "
             "и 50 Мп с 5-кратным оптическим приближением; цифровой зум — до 100×. Фронтальная камера — 12 Мп. "
             "Аккумулятор на 5000 мА·ч заряжается по проводу мощностью до 45 Вт. Размеры — 162,8×77,6×8,2 мм, вес 218 г. "
             "В этом поколении у S Pen нет Bluetooth, поэтому жесты Air actions и удалённый спуск затвора недоступны.",
             "Следующее поколение — {link_samsung_galaxy_s26_ultra}."],
            ["В ATOMM смартфон есть в цветах: {colors}.", "Встроенная память — {mems}.",
             "Страницы по объёму: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета Galaxy S25 Ultra есть в наличии?",
             ["Сейчас в наличии: {colors}."]),
            ("Чем S25 Ultra отличается от S26 Ultra?",
             ["Экран 6,9 дюйма QHD+ и аккумулятор на 5000 мА·ч у моделей одинаковые. У S26 Ultra более новый чип — "
              "Snapdragon 8 Elite Gen 5 for Galaxy, более светосильная основная камера (ƒ/1.4 против ƒ/1.7), зарядка "
              "до 60 Вт вместо 45 Вт и режим Privacy Display. S25 Ultra чуть толще и тяжелее: 8,2 мм и 218 г против "
              "7,9 мм и 214 г."]),
            ("Работает ли S Pen как пульт для камеры?",
             ["Нет. У S Pen в Galaxy S25 Ultra нет Bluetooth, поэтому удалённый спуск затвора и жесты Air actions "
              "не поддерживаются. Писать и рисовать на экране пером можно, как и раньше."]),
        ],
    },
    "samsung-galaxy-s26": {
        "h2": "Galaxy S26: компактный флагман",
        "paras": [
            ["Самая компактная модель флагманской серии Samsung 2026 года. Экран Dynamic AMOLED 2X диагональю 6,3 дюйма "
             "с разрешением FHD+, адаптивной частотой от 1 до 120 Гц и яркостью до 2600 нит закрыт стеклом Corning "
             "Gorilla Glass Victus 2. Алюминиевая рамка, вес 167 г при толщине 7,2 мм — смартфон удобно держать "
             "одной рукой. Защита от воды и пыли — IP68."],
            ["Процессор зависит от рынка: Exynos 2600 или Snapdragon 8 Elite Gen 5 for Galaxy. "
             "Оперативная память — 12 ГБ. Камеры те же, что у старшей S26+: основная 50 Мп (ƒ/1.8), сверхширокоугольная 12 Мп и телефото "
             "10 Мп с 3-кратным оптическим приближением, фронтальная — 12 Мп. Аккумулятор на 4300 мА·ч заряжается "
             "по проводу мощностью до 25 Вт и без проводов — до 15 Вт; по данным Samsung, заряда хватает "
             "до 30 часов воспроизведения видео.",
             "Нужен экран крупнее и батарея ёмче — посмотрите {link_samsung_galaxy_s26_plus}.",
             "Перо S Pen, камера 200 Мп и экран 6,9 дюйма есть у {link_samsung_galaxy_s26_ultra}."],
            ["В ATOMM смартфон есть в цветах: {colors}.", "Встроенная память — {mems}.",
             "Страницы по объёму: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета Galaxy S26 есть в наличии?",
             ["Сейчас в наличии: {colors}."]),
            ("Что выбрать: S26 или S26+?",
             ["Чип, 12 ГБ оперативной памяти и камеры у моделей одинаковые. S26+ берут ради экрана 6,7 дюйма "
              "с разрешением QHD+ вместо 6,3 дюйма FHD+, аккумулятора на 4900 мА·ч вместо 4300 мА·ч и более быстрой "
              "зарядки — 45 Вт против 25 Вт. Базовая модель легче: 167 г против 190 г."]),
            ("Входит ли зарядное устройство в комплект?",
             ["Нет, адаптер питания продаётся отдельно. Для максимальной скорости 25 Вт нужен совместимый адаптер "
              "и кабель USB-C с поддержкой 3 А."]),
        ],
    },
    "samsung-galaxy-s26-plus": {
        "h2": "Galaxy S26+: большой экран без Ultra",
        "paras": [
            ["Средняя модель серии S 2026 года — для тех, кому нужен большой экран, но не нужны перо и камера 200 Мп. "
             "Дисплей Dynamic AMOLED 2X диагональю 6,7 дюйма получил разрешение QHD+ — выше, чем у базовой S26, — "
             "частоту от 1 до 120 Гц и яркость до 2600 нит. Спереди — Corning Gorilla Glass Victus 2, рамка "
             "алюминиевая, защита по IP68. Размеры — 158,4×75,8×7,3 мм, вес 190 г."],
            ["Главное отличие от младшей модели — питание. Аккумулятор на 4900 мА·ч заряжается по проводу мощностью "
             "до 45 Вт: по данным Samsung, за 30 минут — примерно до 69%. Беспроводная зарядка — до 20 Вт, есть "
             "и обратная зарядка Wireless PowerShare для наушников или часов. Процессор в зависимости от рынка — "
             "Exynos 2600 или Snapdragon 8 Elite Gen 5 for Galaxy. Оперативная память — 12 ГБ. Камеры: основная 50 Мп (ƒ/1.8), "
             "сверхширокоугольная 12 Мп и телефото 10 Мп с 3-кратным приближением.",
             "Компактная версия с теми же камерами — {link_samsung_galaxy_s26}.",
             "Флагман серии — {link_samsung_galaxy_s26_ultra}."],
            ["В ATOMM смартфон есть в цветах: {colors}.", "Встроенная память — {mems}.",
             "Страницы по объёму: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета Galaxy S26+ есть в наличии?",
             ["Сейчас в наличии: {colors}."]),
            ("Чем S26+ отличается от S26?",
             ["У смартфона экран 6,7 дюйма QHD+ против 6,3 дюйма FHD+, аккумулятор на 4900 мА·ч вместо 4300 мА·ч, "
              "зарядка до 45 Вт по проводу и до 20 Вт без проводов против 25 и 15 Вт. По данным Samsung, смартфон "
              "воспроизводит видео до 31 часа против 30 у S26. Чип, память и камеры одинаковые."]),
            ("Чем S26+ отличается от S26 Ultra?",
             ["У Ultra экран больше — 6,9 дюйма, основная камера 200 Мп, второй телефото с 5-кратным приближением, "
              "перо S Pen в корпусе, режим Privacy Display, аккумулятор на 5000 мА·ч и зарядка до 60 Вт. "
              "Зато смартфон легче — 190 г против 214 г."]),
        ],
    },
    "samsung-galaxy-z-fold8": {
        "h2": "Galaxy Z Fold8: широкий складной формат",
        "paras": [
            ["Z Fold8 — новый формат в линейке, представленный в июле 2026 года вместе с Fold8 Ultra. Смартфон шире "
             "привычных «книжек»: внешний экран 5,5 дюйма (1248×1972) с соотношением сторон около 10:16 похож "
             "на экран обычного телефона, а внутренний 7,6 дюйма (1848×2448) открывается в формате около 4:3 — "
             "удобно для чтения, таблиц и видео. Оба экрана Dynamic AMOLED 2X с частотой до 120 Гц."],
            ["Внутри — Snapdragon 8 Elite Gen 5 for Galaxy и 12 ГБ оперативной памяти, у версии на 1 ТБ — 16 ГБ. "
             "Сзади две камеры по 50 Мп: основная с оптической стабилизацией и сверхширокоугольная; селфи-камеры "
             "по 10 Мп стоят и на внешнем, и на внутреннем экране. Аккумулятор на 4800 мА·ч заряжается по проводу "
             "до 45 Вт и без проводов до 20 Вт. В сложенном виде корпус — 123,9×81,9×9,7 мм, в разложенном толщина "
             "4,5 мм, вес 201 г. Защита — IP48: смартфон выдерживает погружение в воду, а от пыли защищён лишь "
             "частично. Пера S Pen модель не поддерживает.",
             "Классическая высокая «книжка» с камерой 200 Мп и экраном 8 дюймов — {link_samsung_galaxy_z_fold8_ultra}."],
            ["В ATOMM смартфон есть в цветах: {colors}.", "Встроенная память — {mems}.",
             "Страницы по объёму: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета Galaxy Z Fold8 есть в наличии?",
             ["Сейчас в наличии: {colors}."]),
            ("Чем Z Fold8 отличается от Z Fold8 Ultra?",
             ["Чип, объёмы памяти и мощность проводной зарядки одинаковые. Эта модель шире и ниже: экраны 7,6 и 5,5 дюйма "
              "против 8 и 6,5 дюйма у Ultra, вес 201 г против 215 г, аккумулятор 4800 мА·ч против 5000 мА·ч. "
              "У Ultra три камеры — 200 Мп, сверхширокоугольная 50 Мп и телефото 10 Мп, — а здесь телефото нет."]),
        ],
    },
    "samsung-galaxy-z-flip8": {
        "h2": "Galaxy Z Flip8: раскладушка 2026 года",
        "paras": [
            ["Складной смартфон, который в сложенном виде помещается в ладонь: 75,4×85,7 мм при толщине 13,1 мм. "
             "В разложенном виде толщина — 6,1 мм, а внутри — экран Dynamic AMOLED 2X 6,9 дюйма (2520×1080) "
             "с частотой до 120 Гц. Снаружи — экран Super AMOLED 4,1 дюйма (948×1048) с частотой 60 или 120 Гц."],
            ["По сравнению с Flip7 корпус стал тоньше и легче: 6,1 мм вместо 6,5 мм в разложенном виде и 180 г "
             "вместо 188 г. В зависимости от страны выпуска внутри стоит Exynos 2600 или Snapdragon 8 Elite Gen 5 "
             "for Galaxy, оперативная память — 12 ГБ. Камеры: основная 50 Мп (ƒ/1.8) со стабилизацией, сверхширокоугольная 12 Мп "
             "и фронтальная 10 Мп. Аккумулятор на 4300 мА·ч заряжается по проводу до 25 Вт и без проводов до 15 Вт. "
             "Защита IP48: смартфон защищён от воды, а от пыли — лишь частично.",
             "Прошлое поколение — {link_samsung_galaxy_z_flip7}.",
             "Если нужен складной смартфон с большим экраном-«книжкой», посмотрите {link_samsung_galaxy_z_fold8}."],
            ["В ATOMM смартфон есть в цветах: {colors}.", "Встроенная память — {mems}.",
             "Страницы по объёму: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета Galaxy Z Flip8 есть в наличии?",
             ["Сейчас в наличии: {colors}."]),
            ("Можно ли пользоваться Z Flip8 под дождём и на пляже?",
             ["Под дождём — да: вторая цифра рейтинга IP48 означает защиту от воды, в том числе при погружении. От пыли "
              "и песка он защищён лишь частично — цифра 4 означает защиту от частиц крупнее 1 мм, поэтому на пляже "
              "лучше держать его в чехле или в кармане."]),
        ],
    },
    "apple-macbook-pro-m5-14-16": {
        "h2": "MacBook Pro на M5, M5 Pro и M5 Max: что выбрать",
        "paras": [
            ["MacBook Pro поколения M5 вышел с тремя чипами: базовым M5 (2025) и M5 Pro или M5 Max (март 2026). "
             "Базовая 14-дюймовая модель на M5 получила 10-ядерный процессор, 10-ядерную графику, до 32 ГБ объединённой "
             "памяти и три порта Thunderbolt 4, весит она 1,55 кг. Версии на M5 Pro и M5 Max вышли с диагональю "
             "14 и 16 дюймов. В конце октября 2026 года Apple заменила базовую 14-дюймовую модель версией на M6 "
             "и выпустила MacBook Pro на M5 Pro и M5 Max с OLED-экраном. Ниже — характеристики версий с экраном "
             "Liquid Retina XDR, которые продаются в ATOMM."],
            ["У версий на M5 Pro и M5 Max процессор 15- или 18-ядерный, графика — от 16 до 40 ядер, а порты — три "
             "Thunderbolt 5, HDMI, слот SDXC, MagSafe 3 и разъём для наушников. M5 Pro поддерживает до 64 ГБ памяти, "
             "M5 Max — до 128 ГБ. Экран Liquid Retina XDR с ProMotion до 120 Гц: 14,2 дюйма (3024×1964) или 16,2 дюйма "
             "(3456×2234), до 1000 нит в обычном режиме и до 1600 нит в HDR. Камера — 12 Мп с Center Stage.",
             "Если нужен лёгкий ноутбук без вентилятора, посмотрите {link_apple_macbook_air_m5_13_6} "
             "и {link_apple_macbook_air_m5_15}."],
            ["По данным Apple, дольше всех — до 24 часов потокового видео — работают базовая 14-дюймовая модель на M5 "
             "и 16-дюймовая на M5 Pro; у 16-дюймовой на M5 Max — до 22 часов, у 14-дюймовой на M5 Pro — до 22, "
             "на M5 Max — до 20. Вес 14-дюймовых версий на M5 Pro и M5 Max — "
             "1,60–1,62 кг, 16-дюймовых — 2,14–2,15 кг.",
             "В ATOMM доступны цвета: {colors}.",
             "Чип, объём памяти и накопителя указаны в названии каждого товара."],
        ],
        "faq": [
            ("Какие цвета MacBook Pro на M5 есть в наличии?",
             ["Сейчас в наличии: {colors}."]),
            ("Чем M5 отличается от M5 Pro и M5 Max?",
             ["У M5 10-ядерный процессор и 10-ядерная графика, до 32 ГБ памяти и порты Thunderbolt 4. У M5 Pro — "
              "15 или 18 ядер процессора, 16 или 20 ядер графики и до 64 ГБ памяти, у M5 Max — 18 ядер процессора, "
              "32 или 40 ядер графики и до 128 ГБ памяти. Обе старшие версии получили порты Thunderbolt 5. "
              "Модель 16 дюймов есть только с M5 Pro и M5 Max."]),
            ("Что выбрать: 14 или 16 дюймов?",
             ["16-дюймовая модель даёт больший экран и, по данным Apple, дольше работает: на M5 Pro — до 24 часов "
              "потокового видео против 22 у 14-дюймовой. Зато она тяжелее — 2,14 кг против 1,60 кг. Если ноутбук "
              "часто едет с вами, удобнее 14 дюймов."]),
        ],
    },
    "apple-macbook-air-m5-13-6": {
        "h2": "MacBook Air 13 на M5: лёгкий ноутбук на каждый день",
        "paras": [
            ["Самый компактный MacBook Air 2026 года весит 1,23 кг при толщине 1,13 см. Экран Liquid Retina 13,6 дюйма — "
             "2560×1664 пикселей, 224 ppi, яркость 500 нит, поддержка широкого цветового охвата P3 и True Tone. "
             "Внутри — чип M5 с 10-ядерным процессором (4 высокопроизводительных ядра и 6 энергоэффективных), 8- или "
             "10-ядерной графикой в зависимости от конфигурации и 16-ядерным Neural Engine. Базовая версия получает "
             "16 ГБ объединённой памяти и SSD на 512 ГБ."],
            ["По данным Apple, аккумулятор на 53,8 Вт·ч обеспечивает до 18 часов потокового видео или до 15 часов "
             "веб-сёрфинга по Wi-Fi. Порты — два Thunderbolt 4 (USB-C) до 40 Гбит/с и MagSafe 3, есть разъём "
             "для наушников. Ноутбук подключается к двум внешним мониторам до 6K при 60 Гц, не отключая встроенный "
             "экран. Камера — 12 Мп с Center Stage и Desk View, звук — четыре динамика и три микрофона, Touch ID "
             "встроен в клавиатуру. Wi-Fi 7 и Bluetooth 6 обеспечивает чип Apple N1.",
             "Тот же чип с экраном 15,3 дюйма и шестью динамиками — {link_apple_macbook_air_m5_15}.",
             "Для тяжёлых задач — {link_apple_macbook_pro_m5_14_16}."],
            ["В ATOMM доступны цвета: {colors}.",
             "Объём памяти и накопителя указан в названии каждого товара."],
        ],
        "faq": [
            ("Какие цвета MacBook Air 13 на M5 есть в наличии?",
             ["Сейчас в наличии: {colors}."]),
            ("Сколько внешних мониторов поддерживает MacBook Air на M5?",
             ["До двух: оба с разрешением до 6K при 60 Гц или до 4K при 144 Гц. Один монитор можно подключить "
              "с разрешением до 8K при 60 Гц или 5K при 120 Гц. Встроенный экран при этом продолжает работать."]),
        ],
    },
    "apple-macbook-air-m5-15": {
        "h2": "MacBook Air 15 на M5: большой экран в тонком корпусе",
        "paras": [
            ["Старший MacBook Air 2026 года — для тех, кто много работает с документами, таблицами и фото, но не хочет "
             "носить тяжёлый ноутбук. Экран Liquid Retina 15,3 дюйма — 2880×1864 пикселей, 224 ppi и 500 нит, с цветовым "
             "охватом P3 и True Tone. При этом толщина — 1,15 см, "
             "вес — 1,51 кг."],
            ["Чип M5 здесь идёт с 10-ядерным процессором и 10-ядерной графикой, база — 16 ГБ объединённой памяти "
             "и SSD на 512 ГБ. Аккумулятор ёмче, чем у 13-дюймовой версии, — 66,5 Вт·ч, но по данным Apple время "
             "работы то же: до 18 часов видео и до 15 часов веб-сёрфинга. Звук — шесть динамиков, в том числе вуферы с компенсацией вибраций. Порты — два Thunderbolt 4 (USB-C), "
             "MagSafe 3 и разъём для наушников; поддерживаются два внешних монитора до 6K. Камера 12 Мп с Center "
             "Stage, Wi-Fi 7 и Bluetooth 6 через чип Apple N1, Touch ID.",
             "Если важнее компактность, посмотрите {link_apple_macbook_air_m5_13_6} — он легче на 280 г.",
             "Больше портов и производительности — у {link_apple_macbook_pro_m5_14_16}."],
            ["В ATOMM доступны цвета: {colors}.",
             "Объём памяти и накопителя указан в названии каждого товара."],
        ],
        "faq": [
            ("Какие цвета MacBook Air 15 на M5 есть в наличии?",
             ["Сейчас в наличии: {colors}."]),
            ("MacBook Air 13 или 15 на M5 — что выбрать?",
             ["Процессор и время работы у них одинаковые. 15-дюймовая модель даёт больший экран, шесть динамиков "
              "вместо четырёх и всегда 10-ядерную графику, но весит 1,51 кг против 1,23 кг. Для поездок и учёбы "
              "удобнее 13 дюймов, для работы дома и в офисе — 15."]),
        ],
    },
    "apple-ipad-air-11-2026": {
        "h2": "iPad Air 11 на M4: что важно знать",
        "paras": [
            ["Apple представила этот iPad Air в марте 2026 года. Внутри — чип M4 (8-ядерный процессор, 9-ядерная "
             "графика) и 12 ГБ объединённой памяти: это в полтора раза больше, чем у iPad Air на M3. По данным Apple, "
             "новинка до 30% быстрее предшественника на M3 и быстрее iPad Air на M1 до 2,3 раза. Экран Liquid Retina "
             "11 дюймов (2360×1640 точек, 264 ppi) с яркостью 500 нит."],
            ["Толщина корпуса — 6,1 мм, вес — 464 г у версии Wi-Fi и 465 г у версии с сотовой связью. Touch ID встроен "
             "в верхнюю кнопку, фронтальная камера 12 Мп с Center Stage стоит на длинной стороне — удобно для "
             "видеозвонков, когда планшет лежит горизонтально. Поддерживаются Apple Pencil Pro и Apple Pencil (USB-C), "
             "а также клавиатура Magic Keyboard. За Wi-Fi 7 и Bluetooth 6 отвечает чип Apple N1, разъём USB-C работает "
             "на скорости до 10 Гбит/с. По данным Apple, заряда хватает до 10 часов веб-сёрфинга или видео по Wi-Fi.",
             "Тот же планшет с экраном 13 дюймов — {link_apple_ipad_air_13_2026}.",
             "Если нужны экран Ultra Retina XDR и Face ID, посмотрите {link_apple_ipad_pro_11_m5_2025}."],
            ["В ATOMM доступны цвета: {colors}.", "Объём памяти — {mems}.",
             "Версии с сотовой связью работают в сетях 5G и только с eSIM — физическую SIM-карту в них не вставить.",
             "Выбрать по памяти: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета iPad Air 11 на M4 есть в наличии?",
             ["Сейчас в наличии: {colors}."]),
            ("Можно ли вставить SIM-карту в iPad Air на M4?",
             ["Нет. Версия Wi-Fi + Cellular работает только с eSIM и не поддерживает физические SIM-карты. "
              "Перед покупкой уточните у оператора, выдаёт ли он eSIM для планшета. Версии только с Wi-Fi "
              "к мобильной сети не подключаются."]),
            ("Чем iPad Air на M4 отличается от iPad Air на M3?",
             ["Новая модель получила чип M4 и 12 ГБ памяти вместо 8 ГБ — по данным Apple, она до 30% быстрее. "
              "Впервые в iPad Air появился чип N1 с Wi-Fi 7 и Bluetooth 6, а сотовые версии получили модем Apple C1X: "
              "по данным Apple, мобильный интернет работает до 50% быстрее, чем у iPad Air на M3.",
              "Прошлая модель по-прежнему в продаже — {link_apple_ipad_air_11_2025}."]),
        ],
    },
    "apple-ipad-air-13-2026": {
        "h2": "iPad Air 13 на M4: коротко о главном",
        "paras": [
            ["Самый крупный iPad Air 2026 года. Экран Liquid Retina 13 дюймов — 2732×2048 точек при 264 ppi, яркость "
             "600 нит: на 100 нит больше, чем у 11-дюймовой версии. Начинка та же, что у младшей модели: чип M4 "
             "с 8-ядерным процессором и 9-ядерной графикой, 12 ГБ объединённой памяти. По данным Apple, M4 работает "
             "до 30% быстрее M3."],
            ["При толщине 6,1 мм планшет весит 616 г, с сотовым модулем — 617 г. Большая диагональ выручает, когда "
             "два приложения открыты рядом, при монтаже видео и рисовании: поддерживаются Apple Pencil Pro и Apple "
             "Pencil (USB-C) с наведением, а Magic Keyboard для iPad Air 13 дюймов добавляет трекпад и ряд из 14 "
             "функциональных клавиш. Через USB-C (USB 3, до 10 Гбит/с) подключается внешний монитор до 6K при 60 Гц. "
             "Обе камеры — 12 Мп, фронтальная с Center Stage расположена в альбомной ориентации, стереодинамики "
             "тоже рассчитаны на горизонтальное положение. Wi-Fi 7 и Bluetooth 6 обеспечивает чип Apple N1, сотовые "
             "версии получили модем Apple C1X с 5G. Apple обещает до 10 часов веб-сёрфинга или видео по Wi-Fi.",
             "Тот же M4 в компактном корпусе — {link_apple_ipad_air_11_2026}.",
             "Предыдущее поколение 13-дюймового Air на M3 — {link_apple_ipad_air_13_2025}."],
            ["Цвета в ATOMM: {colors}.", "Память — {mems}.",
             "Модели Wi-Fi + Cellular работают только с eSIM.",
             "Страницы по объёму: {mem_links}."],
        ],
        "faq": [
            ("iPad Air 13 или 11 дюймов на M4 — что выбрать?",
             ["Производительность у них одинаковая: чип M4 и 12 ГБ памяти. 13-дюймовая модель даёт больший и более "
              "яркий экран — 600 нит против 500, — но весит 616 г против 464 г у 11-дюймовой. Для работы за столом "
              "и рисования удобнее 13 дюймов, для поездок и чтения в руках — 11.",
              "Компактная версия — {link_apple_ipad_air_11_2026}."]),
            ("Можно ли подключить iPad Air 13 к монитору?",
             ["Да. Через порт USB-C с поддержкой DisplayPort планшет выводит изображение на один внешний дисплей "
              "с разрешением до 6K при 60 Гц."]),
            ("Вставляется ли в iPad Air 13 SIM-карта?",
             ["Нет, у сотовых версий нет лотка: связь 5G подключается только через eSIM. По данным Apple, в мобильной "
              "сети заряда хватает до 9 часов веб-сёрфинга. Версия Wi-Fi выходит в интернет только через Wi-Fi "
              "или режим модема телефона."]),
        ],
    },
    "apple-ipad-air-11-2025": {
        "h2": "iPad Air 11 на M3: кому подойдёт",
        "paras": [
            ["Прошлое поколение iPad Air, вышедшее весной 2025 года, — для тех, кому нужен планшет на чипе серии M, "
             "но не обязательны новшества версии на M4: 12 ГБ памяти, Wi-Fi 7 и модем C1X. Здесь стоит M3 "
             "с 8-ядерным процессором (4 производительных и 4 энергоэффективных ядра), 9-ядерной графикой с аппаратной "
             "трассировкой лучей и 8 ГБ оперативной памяти. По данным Apple, он почти вдвое быстрее iPad Air на M1 "
             "и поддерживает Apple Intelligence."],
            ["Для учёбы, рукописных конспектов и рисования планшет совместим с Apple Pencil Pro и Apple Pencil (USB-C), "
             "а Magic Keyboard для iPad Air в версии 2025 года получила увеличенный трекпад и ряд функциональных клавиш. "
             "Экран Liquid Retina 11 дюймов — 2360×1640 точек, 264 ppi, 500 нит, широкий цветовой охват P3 и True Tone. "
             "Корпус весит 460 г в любой версии, камеры — по 12 Мп, основная снимает 4K. USB-C работает как USB 3 "
             "до 10 Гбит/с, по воздуху — Wi-Fi 6E и Bluetooth 5.3. По данным Apple, автономность — до 10 часов "
             "веб-сёрфинга или просмотра видео по Wi-Fi.",
             "Преемник с 12 ГБ памяти и Wi-Fi 7 — {link_apple_ipad_air_11_2026}.",
             "Если нужен планшет проще — {link_apple_ipad_11_2025}."],
            ["В наличии цвета: {colors}.", "Варианты памяти — {mems}.",
             "Сотовые версии — только с eSIM, слота для SIM-карты в них нет.",
             "По объёму: {mem_links}."],
        ],
        "faq": [
            ("Стоит ли брать iPad Air на M3, если вышел M4?",
             ["Да, если планшет нужен для учёбы, заметок, фото и видео — с этим M3 справляется. "
              "Модель на M4 даёт 12 ГБ памяти вместо 8, Wi-Fi 7 и, по данным Apple, работает до 30% быстрее: это "
              "заметно в тяжёлых приложениях и даёт запас на годы.",
              "Новая модель — {link_apple_ipad_air_11_2026}."]),
            ("Чем iPad Air на M3 лучше базового iPad 11?",
             ["У Air чип M3 вместо A16, поддержка Apple Pencil Pro, USB-C со скоростью USB 3 (у базового iPad — USB 2) "
              "и Wi-Fi 6E вместо Wi-Fi 6. Корпус тоньше и легче: 6,1 мм и 460 г против 7 мм и 477 г.",
              "Сравните с {link_apple_ipad_11_2025}."]),
        ],
    },
    "apple-ipad-11-2025": {
        "h2": "iPad 11 (A16): кому подойдёт",
        "paras": [
            ["Базовый iPad 2025 года — самая простая модель линейки с экраном 11 дюймов. Дисплей "
             "Liquid Retina с разрешением 2360×1640 точек (264 ppi) и яркостью 500 нит, внутри — чип A16 "
             "с 5-ядерным процессором и 4-ядерной графикой."],
            ["Корпус толщиной 7 мм весит 477 г, версия с сотовой связью — 481 г. Обе камеры по 12 Мп; фронтальная "
             "с Center Stage расположена в альбомной ориентации, поэтому в видеозвонке вы остаётесь в центре кадра, даже "
             "когда планшет стоит в чехле-клавиатуре горизонтально. Для набора текста Apple выпускает Magic Keyboard Folio "
             "с трекпадом и рядом из 14 функциональных клавиш. Из стилусов поддерживаются Apple Pencil (USB-C) "
             "и Apple Pencil первого поколения — ему нужен переходник с USB-C. Порт USB-C работает на скорости "
             "USB 2 (до 480 Мбит/с) и выводит изображение на монитор до 4K при 60 Гц. Есть Wi-Fi 6 и Touch ID "
             "в верхней кнопке. Apple заявляет, что от одной зарядки планшет проработает до 10 часов веб-сёрфинга или просмотра видео.",
             "Нужен планшет компактнее — посмотрите {link_apple_ipad_mini_2024}.",
             "Мощнее и с поддержкой Apple Pencil Pro — {link_apple_ipad_air_11_2025}."],
            ["Цвета в ATOMM: {colors}.", "Объём памяти — {mems}.",
             "Версии Wi-Fi + Cellular поддерживают 5G и работают только с eSIM.",
             "Варианты по памяти: {mem_links}."],
        ],
        "faq": [
            ("Для чего хватит iPad 11 на A16?",
             ["Для учёбы, фильмов, чтения, видеосвязи и рукописных заметок. Если планируете монтаж видео, сложную "
              "графику или работу с внешним монитором как с основным экраном, присмотритесь к iPad Air на чипах M.",
              "Например, {link_apple_ipad_air_11_2025}."]),
            ("Поддерживает ли iPad 11 Apple Pencil Pro?",
             ["Нет. С ним работают Apple Pencil (USB-C) и Apple Pencil первого поколения — последний подключается "
              "через переходник USB-C to Apple Pencil Adapter. Apple Pencil Pro поддерживают, например, "
              "iPad mini на A17 Pro и iPad Air на M3 и M4."]),
        ],
    },
    "apple-ipad-mini-2024": {
        "h2": "iPad mini на A17 Pro: главное",
        "paras": [
            ["Компактный iPad осени 2024 года с экраном Liquid Retina 8,3 дюйма: 2266×1488 точек, 326 ppi — "
             "плотнее, чем у 11-дюймовых iPad с их 264 ppi, — яркость 500 нит и антибликовое покрытие. Чип A17 Pro "
             "объединяет 6-ядерный процессор, 5-ядерную графику и 16-ядерную Neural Engine. По данным Apple, "
             "по сравнению с прошлым iPad mini процессор быстрее на 30%, графика — на 25%, а Neural Engine — вдвое; "
             "планшет поддерживает Apple Intelligence."],
            ["Размеры — 195,4×134,8 мм при толщине 6,3 мм, вес — 293 г (297 г у сотовой версии): планшет держат "
             "одной рукой и носят в небольшой сумке. Он совместим с Apple Pencil Pro и Apple Pencil (USB-C) "
             "с наведением — удобно для заметок и набросков на ходу. Фирменной клавиатуры для mini у Apple нет, "
             "подойдёт любая Bluetooth-клавиатура. USB-C — USB 3 до 10 Гбит/с, по данным Apple вдвое быстрее, "
             "чем у предыдущего mini; беспроводная связь — Wi-Fi 6E и Bluetooth 5.3. Основная камера 12 Мп снимает "
             "4K до 60 кадров/с, фронтальная 12 Мп — с Center Stage. По данным Apple, заряда хватает до 10 часов "
             "веб-сёрфинга или просмотра видео по Wi-Fi.",
             "С экраном 11 дюймов — {link_apple_ipad_11_2025}."],
            ["Сейчас в наличии цвета: {colors}.", "Память — {mems}.",
             "Модели с сотовой связью — только eSIM.",
             "Выбрать по объёму: {mem_links}."],
        ],
        "faq": [
            ("iPad mini или iPad 11 — что выбрать?",
             ["iPad mini выбирают за размер: 8,3 дюйма и 293 г против 11 дюймов и 477 г. Кроме того, у него чип A17 Pro "
              "с поддержкой Apple Intelligence, совместимость с Apple Pencil Pro и USB-C со скоростью USB 3. "
              "iPad 11 даёт больший экран и клавиатуру Magic Keyboard Folio — с ним удобнее печатать и смотреть фильмы.",
              "Подробнее — {link_apple_ipad_11_2025}."]),
            ("Сколько памяти брать в iPad mini?",
             ["Базовый объём — вдвое больше, чем у прошлого поколения, — подойдёт для книг, приложений "
              "и потокового видео. Старшие версии стоит брать, если храните на планшете фильмы в дорогу, большие "
              "игры или фотоархив.",
              "В наличии: {mems}."]),
        ],
    },
    "apple-iphone-15": {
        "h2": "iPhone 15: что нужно знать",
        "paras": [
            ["Базовый iPhone 2023 года с Dynamic Island и разъёмом USB-C. Экран OLED 6,1 дюйма (2556×1179 точек, "
             "460 ppi): обычная яркость — до 1000 нит, в HDR — до 1600 нит, на улице — до 2000 нит. Внутри — чип "
             "A16 Bionic с 6-ядерным процессором, 5-ядерной графикой и 16-ядерной Neural Engine."],
            ["Сзади две камеры. Основная 48 Мп (ƒ/1.6) со стабилизацией сдвигом матрицы снимает и с 2-кратным "
             "приближением в 12 Мп, сверхширокоугольная 12 Мп охватывает 120°. Фронтальная камера — 12 Мп, видео — "
             "до 4K Dolby Vision при 60 кадрах/с. Корпус алюминиевый, заднее стекло окрашено в массе, спереди Ceramic "
             "Shield, защита IP68 — до 6 м на 30 минут. Размеры — 147,6×71,6×7,8 мм, вес 171 г. По данным Apple, "
             "заряда хватает до 20 часов воспроизведения видео; USB-C работает на скорости USB 2. Функции Apple "
             "Intelligence на этой модели недоступны: Apple поддерживает их начиная с iPhone 15 Pro и линейки iPhone 16.",
             "Если они нужны, посмотрите {link_apple_iphone_16}.",
             "Тот же чип с экраном 6,7 дюйма — {link_apple_iphone_15_plus}."],
            ["В ATOMM есть цвета: {colors}.", "Объём памяти — {mems}.", "{sim}",
             "Страницы по памяти: {mem_links}."],
        ],
        "faq": [
            ("Какие цвета iPhone 15 есть в наличии?",
             ["В наличии: {colors}."]),
            ("Есть ли iPhone 15 с физической SIM-картой?",
             ["{sim_answer}"]),
            ("Чем iPhone 15 отличается от iPhone 16?",
             ["У iPhone 16 чип A18 вместо A16, поддержка Apple Intelligence и кнопки Action и Camera Control. По данным "
              "Apple, он воспроизводит видео до 22 часов против 20. Экран 6,1 дюйма, основная камера 48 Мп и USB-C "
              "со скоростью USB 2 у моделей одинаковые."]),
        ],
    },
    "apple-iphone-16e": {
        "h2": "Коротко об iPhone 16e",
        "paras": [
            ["Доступный iPhone 2025 года с поддержкой Apple Intelligence. Экран OLED 6,1 дюйма (2532×1170 точек, "
             "460 ppi): до 800 нит в обычном режиме и до 1200 нит в HDR. Внутри — чип A18 с 6-ядерным процессором "
             "и 4-ядерной графикой, а за связь отвечает модем Apple C1 собственной разработки."],
            ["Сзади одна камера — 48 Мп Fusion (ƒ/1.6) с оптической стабилизацией; она же снимает с 2-кратным "
             "приближением в 12 Мп. Фронтальная камера 12 Мп получила автофокус. Есть Face ID, кнопка Action "
             "и защита IP68 — до 6 м на 30 минут. Размеры — 146,7×71,5×7,8 мм, вес 167 г. По данным Apple, "
             "заряда хватает до 26 часов воспроизведения видео, а с адаптером от 20 Вт батарея заряжается до 50% "
             "за 30 минут. Беспроводная зарядка — по стандарту Qi, USB-C работает на скорости USB 2.",
             "Преемник с чипом A19 и MagSafe — {link_apple_iphone_17e}."],
            ["Цвета в ATOMM: {colors}.", "Объём памяти — {mems}.", "{sim}",
             "Выбрать по памяти: {mem_links}."],
        ],
        "faq": [
            ("Есть ли iPhone 16e с физической SIM-картой?",
             ["{sim_answer}"]),
            ("Что выбрать: iPhone 16e или iPhone 16?",
             ["У iPhone 16 вторая, сверхширокоугольная камера 12 Мп, Dynamic Island, кнопка Camera Control и MagSafe. "
              "Чип у обоих — A18, но у 16e графика 4-ядерная. Зато 16e дольше работает: до 26 часов видео против 22 "
              "и легче — 167 г против 170 г.",
              "Сравните с {link_apple_iphone_16}."]),
        ],
    },
    "apple-ipad-pro-13-m5-2025": {
        "h2": "iPad Pro 13 на M5: главное",
        "paras": [
            ["Самый большой iPad 2025 года. Экран Ultra Retina XDR 13 дюймов сделан на двухслойной (tandem) OLED-матрице: "
             "2752×2064 точек, 264 ppi, ProMotion с частотой от 10 до 120 Гц, до 1000 нит в обычном режиме и до 1600 нит "
             "в HDR. Версии на 1 и 2 ТБ можно взять с нанотекстурным стеклом, которое гасит блики."],
            ["Конфигурация чипа M5 зависит от объёма: у версий на 256 и 512 ГБ 9-ядерный процессор и 12 ГБ "
             "объединённой памяти, у версий на 1 и 2 ТБ — 10-ядерный процессор и 16 ГБ. Графика везде 10-ядерная. "
             "При толщине 5,1 мм планшет весит 579 г, с сотовым модулем — 582 г. Порт Thunderbolt / USB 4 передаёт "
             "данные со скоростью до 40 Гбит/с и выводит изображение на монитор до 6K при 60 Гц. Беспроводная часть — "
             "чип Apple N1 (Wi-Fi 7, Bluetooth 6), а в версиях с мобильной связью стоит 5G-модем Apple C1X. Есть Face ID, сканер LiDAR, "
             "поддержка Apple Pencil Pro и Apple Pencil (USB-C). По данным Apple, батареи хватает до 10 часов "
             "веб-сёрфинга или видео по Wi-Fi.",
             "Тот же M5 в компактном корпусе — {link_apple_ipad_pro_11_m5_2025}.",
             "Если хватит чипа попроще — {link_apple_ipad_air_13_2026}."],
            ["Цвета в ATOMM: {colors}.", "Память — {mems}.",
             "Для мобильного интернета нужна eSIM: лотка под SIM-карту в сотовых версиях нет.",
             "Страницы по объёму: {mem_links}."],
        ],
        "faq": [
            ("Для каких версий есть нанотекстурное стекло?",
             ["Только для версий на 1 и 2 ТБ. Матовое покрытие рассеивает отражения, и с планшетом удобнее работать "
              "при ярком свете. В названии такого товара указано «с нанотекстурой»."]),
            ("Чем 13-дюймовый iPad Pro отличается от 11-дюймового?",
             ["Чип, камеры, порт и варианты памяти одинаковые. 13-дюймовая модель даёт больший экран — 2752×2064 точек "
              "против 2420×1668, — но весит 579 г против 444 г. Для монтажа, рисования и работы с двумя приложениями "
              "рядом удобнее 13 дюймов, для поездок — 11.",
              "Компактная версия — {link_apple_ipad_pro_11_m5_2025}."]),
        ],
    },
    "apple-ipad-pro-11-m5-2025": {
        "h2": "iPad Pro 11 на M5: коротко",
        "paras": [
            ["Компактная версия iPad Pro 2025 года. Экран Ultra Retina XDR 11 дюймов — tandem OLED с разрешением "
             "2420×1668 точек (264 ppi), ProMotion от 10 до 120 Гц, яркостью до 1000 нит в обычном режиме и до 1600 нит "
             "в HDR, с широким цветовым охватом P3 и True Tone. Нанотекстурное стекло доступно для версий на 1 и 2 ТБ."],
            ["Чип M5 с 10-ядерной графикой: в версиях на 256 и 512 ГБ — 9-ядерный процессор и 12 ГБ памяти, "
             "в версиях на 1 и 2 ТБ — 10-ядерный и 16 ГБ. Толщина корпуса — 5,3 мм, вес — 444 г (446 г у сотовой "
             "версии), так что планшет удобно держать в руках. Разъём Thunderbolt / USB 4 работает со скоростью "
             "до 40 Гбит/с. За Wi-Fi 7, Bluetooth 6 и Thread отвечает чип Apple N1, у сотовых версий — модем Apple C1X "
             "с 5G. По данным Apple, заряда хватает до 10 часов веб-сёрфинга или видео по Wi-Fi и до 9 часов "
             "веб-сёрфинга в сотовой сети; с адаптером от 60 Вт батарея заряжается до 50% примерно за 30 минут.",
             "Нужен экран больше — {link_apple_ipad_pro_13_m5_2025}.",
             "Дешевле и с чипом M4 — {link_apple_ipad_air_11_2026}."],
            ["В наличии цвета: {colors}.", "Варианты памяти — {mems}.",
             "Сотовая связь в этих планшетах работает через eSIM.",
             "По объёму: {mem_links}."],
        ],
        "faq": [
            ("Сколько оперативной памяти в iPad Pro 11 на M5?",
             ["Зависит от накопителя: 12 ГБ в версиях на 256 и 512 ГБ и 16 ГБ — в версиях на 1 и 2 ТБ. У старших "
              "версий и процессор мощнее — 10 ядер вместо 9.",
              "В наличии: {mems}."]),
            ("Можно ли вставить SIM-карту в iPad Pro 11?",
             ["Нет. Версии Wi-Fi + Cellular работают только с eSIM, физическую SIM-карту они не поддерживают. "
              "Версия Wi-Fi выходит в интернет через Wi-Fi или режим модема телефона."]),
        ],
    },
    "apple-mac-mini": {
        "h2": "Mac mini на M6 и M4: что выбрать",
        "paras": [
            ["Компактный настольный компьютер Apple: корпус 12,7×12,7 см высотой 5 см, монитор, клавиатуру и мышь "
             "подключают свои. В августе 2026 года Apple обновила модель, продажи начались 22 сентября. Новая версия "
             "работает на чипе M6 — первом 2-нанометровом чипе Apple: 12-ядерный процессор (на два ядра больше, чем "
             "у M4), 12-ядерная графика с нейроускорителями в каждом ядре и от 16 ГБ объединённой памяти."],
            ["По данным Apple, M6 до 40% быстрее M4 в многопоточных задачах, а графика — вдвое. Сзади — три порта "
             "Thunderbolt 4, HDMI и Ethernet 2,5 Гбит/с, спереди — два USB-C (USB 3 до 10 Гбит/с) и разъём для "
             "наушников. Беспроводной модуль — собственный чип Apple N1 с поддержкой Wi-Fi 7 и Bluetooth 6. Можно подключить до трёх мониторов: "
             "например, два 6K и третий 5K при 60 Гц.",
             "Компьютер со встроенным экраном — в разделе {link_monobloki_apple_imac}."],
            ["В ATOMM есть и предыдущее поколение 2024 года в том же корпусе — на M4 (10-ядерные процессор и графика) "
             "и M4 Pro (12-ядерный процессор, 16-ядерная графика, порты Thunderbolt 5). У них Wi-Fi 6E, Bluetooth 5.3 "
             "и гигабитный Ethernet. Какой чип стоит в конкретном компьютере и сколько у него памяти и места на SSD, "
             "видно прямо в карточке товара."],
        ],
        "faq": [
            ("Что выбрать: M6 или M4 Pro?",
             ["M6 новее: у него Wi-Fi 7, Bluetooth 6 и Ethernet 2,5 Гбит/с. У M4 Pro больше ядер графики (16 против 12), "
              "24 ГБ памяти в базовой версии, более широкая полоса памяти — 273 ГБ/с против 153–170 ГБ/с у M6 (зависит "
              "от объёма памяти) — и порты "
              "Thunderbolt 5 до 120 Гбит/с, что пригодится для быстрых внешних накопителей и мониторов."]),
            ("Что нужно докупить к компьютеру?",
             ["Монитор, клавиатуру и мышь или трекпад: компьютер поставляется без них. Подойдут мониторы с HDMI, USB-C "
              "или Thunderbolt и клавиатуры с Bluetooth или USB."]),
        ],
    },
    "airpods-pro-3": {
        "h2": "AirPods Pro 3: что нового",
        "paras": [
            ["Третье поколение Pro-наушников Apple работает на чипе H2. По данным Apple, активное шумоподавление стало "
             "до 2 раз эффективнее, чем у AirPods Pro 2. Амбушюры теперь с пенным наполнителем, в комплекте пять размеров — "
             "от XXS до L, так что посадку проще подобрать под своё ухо. Каждый наушник весит 5,55 г."],
            ["AirPods Pro 3 впервые среди AirPods получили датчик пульса: он отслеживает частоту сердечных сокращений "
             "во время тренировок "
             "и передаёт данные в приложение «Фитнес» на iPhone с iOS 26 или новее. Для замера датчик подсвечивает кожу "
             "невидимым инфракрасным светом 256 раз в секунду. Наушники и кейс защищены от пыли, пота "
             "и воды по IP57. Одного заряда хватает до 8 часов прослушивания с шумоподавлением, вместе с кейсом — "
             "до 24 часов. Кейс MagSafe заряжается через USB-C, от зарядных устройств MagSafe и Qi и даже от зарядки "
             "Apple Watch; внутри есть динамик и чип Ultra Wideband второго поколения для поиска через «Локатор»."],
            ["Другие наушники Apple — {link_airpods_max_2} и {link_airpods_5}."],
        ],
        "faq": [
            ("Подходят ли AirPods Pro 3 для тренировок?",
             ["Да. Наушники защищены от пыли, пота и воды по IP57, а встроенный датчик пульса записывает частоту сердечных "
              "сокращений во время тренировки. С включённым датчиком один заряд держится до 6,5 часа."]),
            ("Чем AirPods Pro 3 отличаются от AirPods Pro 2?",
             ["По данным Apple, шумоподавление стало до 2 раз эффективнее, а время работы с ним выросло на треть — "
              "до 8 часов на одном заряде. Добавились датчик пульса, пенные амбушюры и размер XXS. Общий запас с кейсом "
              "при этом меньше: до 24 часов против 30 часов у Pro 2."]),
            ("Как заряжать кейс?",
             ["Через кабель USB-C или без проводов: от зарядного устройства MagSafe, Qi-совместимой площадки "
              "или зарядки для Apple Watch."]),
        ],
    },
    "apple-watch-ultra-3": {
        "h2": "Apple Watch Ultra 3: коротко о главном",
        "paras": [
            ["Часы для спорта и путешествий с титановым корпусом 49 мм и плоским сапфировым стеклом. Экран Always-On Retina "
             "с широкоугольными OLED и LTPO: яркость до 3000 нит и минимум 1 нит, а в режиме «Всегда включён» изображение "
             "обновляется раз в секунду. Разрешение — 422×514 точек, а экран крупнее, чем у Ultra 2 (1245 против 1185 мм²). "
             "Внутри — чип S10, "
             "вес корпуса — около 62 г."],
            ["По данным Apple, заряда хватает до 42 часов в обычном режиме и до 72 часов в режиме энергосбережения, "
             "а до 80% часы заряжаются примерно за 45 минут. Водонепроницаемость — 100 м по ISO 22810:2010, корпус "
             "защищён от пыли по IP6X и прошёл испытания по MIL-STD 810H. Часы подходят для любительского дайвинга "
             "на глубину до 40 м, а для навигации есть двухчастотный GPS (L1 и L5) и компас.",
             "Следующее поколение — {link_apple_watch_ultra_4}."],
            ["Ремешки и браслеты в наличии: {colors}."],
        ],
        "faq": [
            ("Чем Apple Watch Ultra 3 отличаются от Ultra 2?",
             ["Ultra 3 получили чип S10 вместо S9 и экран с широкоугольными OLED и большей активной областью. "
              "Время работы выросло с 36 до 42 часов, а зарядка до 80% занимает около 45 минут против примерно часа у Ultra 2."]),
            ("Можно ли нырять с этими часами?",
             ["Да, они рассчитаны на любительский дайвинг до 40 м по стандарту EN13319: есть глубиномер, датчик температуры "
              "воды, приложение «Глубина» запускается при погружении, а отсчёт времени погружения начинается на глубине 1 м. "
              "Apple рекомендует использовать часы только для любительских погружений до 40 м."]),
            ("Какие ремешки и браслеты есть в наличии?",
             ["Сейчас в наличии: {colors}."]),
        ],
    },
    # AirPods 4 / AirPods 5: цвета в названиях товаров функцией color_of не разбираются ({colors} пуст) — их не упоминаем
    "airpods-4": {
        "h2": "AirPods 4: обычные или с шумоподавлением",
        "paras": [
            ["AirPods 4 — открытые вкладыши Apple 2024 года без амбушюр. Они выпускаются в двух версиях: обычной "
             "и с активным шумоподавлением. Корпус у них одинаковый: каждый наушник весит 4,3 г, внутри — чип H2 "
             "и Bluetooth 5.3, на ножке — датчик нажатия для управления. Наушники и кейс защищены от пыли, пота и воды "
             "по IP54, так что в них можно заниматься спортом, но не плавать."],
            ["Версия с шумоподавлением, кроме самого шумоподавления, получила режим «Прозрачность», адаптивный звук "
             "и автоматическое приглушение музыки, когда вы начинаете говорить. По данным Apple, она играет до 4 часов "
             "с включённым шумоподавлением и до 5 часов без него, а вместе с кейсом — до 20 и до 30 часов. Её кейс "
             "заряжается по USB-C, от Qi-совместимых зарядок и от зарядки Apple Watch, а встроенный динамик помогает "
             "найти кейс через «Локатор»."],
            ["Обычные AirPods 4 работают до 5 часов на одном заряде и до 30 часов с кейсом. Их кейс легче — 32,3 г "
             "против 34,7 г, но заряжается только по кабелю USB-C. Какая версия перед вами, указано в названии "
             "товара: у версии с активным шумоподавлением в нём есть слова «с шумоподавлением».",
             "Новое поколение — {link_airpods_5}: шумоподавление в нём есть в обеих версиях.",
             "Подробное сравнение — в статье {guide_airpods}."],
        ],
        "faq": [
            ("Чем AirPods 4 с шумоподавлением отличаются от обычных?",
             ["Активным шумоподавлением, режимом «Прозрачность» и адаптивным звуком, а также кейсом: его можно "
              "заряжать без проводов, и в нём есть динамик для поиска через «Локатор». Чип H2, форма и вес наушников "
              "у версий одинаковые. С включённым шумоподавлением наушники работают до 4 часов, без него — до 5 часов, "
              "как и обычные AirPods 4."]),
            ("Как заряжается кейс AirPods 4?",
             ["У обычной версии — только по кабелю USB-C. Кейс версии с шумоподавлением заряжается ещё и от "
              "Qi-совместимых беспроводных зарядок и от зарядки Apple Watch. По данным Apple, 5 минут в кейсе дают "
              "около часа прослушивания."]),
            ("Можно ли заниматься в AirPods 4 спортом?",
             ["Да. Наушники и кейс защищены от пыли, пота и воды по IP54 — этого достаточно для тренировок, "
              "но не для плавания."]),
            ("Что выбрать: AirPods 4 или AirPods 5?",
             ["В AirPods 5 активное шумоподавление есть в обеих версиях и, по данным Apple, убирает до 50% больше шума, "
              "чем у AirPods 4 с шумоподавлением. Без шумоподавления AirPods 5 к тому же дольше работают "
              "от одного заряда: до 6 часов у базовой версии и до 7 часов у версии с кейсом беспроводной зарядки "
              "против 5 часов у AirPods 4.",
              "Все отличия — в статье {guide_airpods}."]),
        ],
    },
    "airpods-5": {
        "h2": "AirPods 5: что нового",
        "paras": [
            ["Пятое поколение открытых вкладышей Apple вышло в сентябре 2026 года. Главное изменение — активное "
             "шумоподавление теперь есть в обеих версиях, включая самую доступную. По данным Apple, оно убирает до 50% "
             "больше шума, чем у AirPods 4 с шумоподавлением. Кроме него, есть режим «Прозрачность», адаптивный звук "
             "и автоматическое приглушение музыки во время разговора. Внутри — чип H2 и Bluetooth 5.3, каждый наушник "
             "весит 4,3 г. Наушники и кейс защищены от пыли, пота и воды по IP57 (у AirPods 4 — IP54)."],
            ["Версии отличаются кейсом и временем работы. В каталоге ATOMM старшая называется «беспроводная зарядка "
             "чехла» — это AirPods 5 с кейсом беспроводной зарядки (Wireless Charging Case). Её кейс заряжается "
             "по USB-C, от Qi-совместимых зарядок и от зарядки Apple Watch, в нём есть динамик для поиска через "
             "«Локатор» (нужна iOS 27 или новее), а громкость можно менять свайпом по ножке наушника. По данным Apple, "
             "эта версия играет до 5 часов с шумоподавлением и до 7 часов без него, а с кейсом — до 22 часов. "
             "У базовой версии кейс заряжается только по USB-C, а запас — до 4 часов с шумоподавлением, до 6 часов "
             "без него и до 20 часов с кейсом."],
            ["Прошлое поколение — {link_airpods_4}.",
             "Чем новинка отличается от него, разобрали в статье {guide_airpods}.",
             "Если нужны внутриканальные наушники с амбушюрами, посмотрите {link_airpods_pro_3}."],
        ],
        "faq": [
            ("Что значит «беспроводная зарядка чехла» в названии?",
             ["Так в каталоге обозначена версия AirPods 5 с кейсом беспроводной зарядки. Кроме USB-C, её кейс "
              "заряжается от Qi-совместимых зарядок и от зарядки Apple Watch, в нём есть динамик для «Локатора», "
              "а наушники работают дольше — до 5 часов с шумоподавлением против 4 часов у базовой версии."]),
            ("Есть ли шумоподавление в базовой версии AirPods 5?",
             ["Да, активное шумоподавление и режим «Прозрачность» есть в обеих версиях AirPods 5. Различаются они "
              "кейсом и временем работы."]),
            ("Чем AirPods 5 отличаются от AirPods 4?",
             ["По данным Apple, шумоподавление убирает до 50% больше шума, чем у AirPods 4 с шумоподавлением, "
              "а версия с кейсом беспроводной зарядки работает с шумоподавлением на час дольше — до 5 часов. Шумоподавление "
              "теперь есть и в самой доступной версии. Вес наушников и чип H2 остались прежними.",
              "Подробнее — в статье {guide_airpods}."]),
            ("Работают ли AirPods 5 с Android?",
             ["Да, как обычные Bluetooth-наушники, но с ограниченным набором функций. Полный набор функций Apple "
              "заявляет для iPhone, iPad, Mac и Apple Watch с последними версиями системы."]),
        ],
    },
    "apple-watch-series-12": {
        "h2": "Apple Watch Series 12: коротко о главном",
        "paras": [
            ["Универсальные часы Apple 2026 года с корпусом 42 или 46 мм. Apple выпускает их в трёх материалах: "
             "алюминий (бронзовый, светлое золото, чёрный и серый космос), титан (золотой и натуральный) и новая для "
             "этого поколения керамика (белый жемчуг и тёмно-синий). Экран Always-On Retina с широкоугольными OLED и LTPO3 — до 2000 нит, "
             "минимум 1 нит. У алюминиевых часов экран закрыт стеклом Ceramic Shield 2, которое, по данным Apple, "
             "на 60% прочнее стекла Ion-X у Series 11, у титановых и керамических — сапфировым стеклом."],
            ["Внутри — чип S11 и 64 ГБ памяти. Главная новинка — система датчиков Health Sensing System: новые "
             "оптический и электрический датчики сердца. По данным Apple, пульс измеряется каждые 5 секунд в течение "
             "дня, а вариабельность сердечного ритма — до 24 раз чаще, чем раньше. Заряда хватает до 24 часов, "
             "в режиме энергосбережения — до 38 часов, а до 80% часы заряжаются примерно за 30 минут. "
             "Водонепроницаемость — 50 м, защита от пыли — IP6X. Для настройки нужен iPhone 11 или новее с iOS 27."],
            ["Ремешки и браслеты в наличии: {colors}.",
             "Для спорта и путешествий есть {link_apple_watch_ultra_4}, прошлое поколение — {link_apple_watch_series_11}."],
        ],
        "faq": [
            ("Какой размер выбрать: 42 или 46 мм?",
             ["46 мм — экран крупнее (416×496 точек против 374×446), корпус подходит на запястье обхватом 140–245 мм. "
              "42 мм легче и рассчитан на запястье 130–200 мм. Алюминиевая версия с GPS весит 32,2 г в размере 42 мм "
              "и 39,5 г в размере 46 мм."]),
            ("Чем алюминий отличается от титана и керамики?",
             ["Цветами, весом и стеклом. Алюминиевые часы самые лёгкие и закрыты стеклом Ceramic Shield 2, титановые "
              "и керамические — сапфировым стеклом. В размере 46 мм титановые весят 44,9 г, керамические — "
              "51,3–52,9 г в зависимости от цвета."]),
            ("Чем Series 12 отличаются от Series 11?",
             ["Новыми датчиками сердца Health Sensing System. По данным Apple, тренировку на улице часы "
              "записывают на 25% дольше — до 10 часов, 15 минут зарядки дают до 12 часов работы (на 50% больше), "
              "а стекло алюминиевых моделей стало на 60% прочнее."]),
            ("Какие ремешки и браслеты есть в наличии?",
             ["Сейчас в наличии: {colors}.", "Размер ремешка указан в названии каждого товара."]),
        ],
    },
    "apple-watch-ultra-4": {
        "h2": "Apple Watch Ultra 4: коротко о главном",
        "paras": [
            ["Часы для спорта и путешествий с корпусом 49 мм из титана Grade 5 — натурального или чёрного цвета — "
             "и плоским сапфировым стеклом. Экран Always-On Retina с широкоугольными OLED и LTPO3: до 3000 нит, "
             "минимум 1 нит, разрешение 422×514 точек, площадь 1245 мм². Внутри — чип S11 и 64 ГБ памяти, вес часов — "
             "около 63 г."],
            ["Главное отличие от прошлых Ultra — автономность. По данным Apple, заряда хватает до 50 часов, в режиме "
             "энергосбережения — до 84 часов, тренировку с GPS часы записывают до 18 часов, а в режиме максимальной "
             "экономии — до 45 часов. До 80% батарея заряжается примерно за 45 минут. Новые "
             "оптический и электрический датчики сердца измеряют пульс каждые 5 секунд в течение всего дня."],
            ["Водонепроницаемость — 100 м по ISO 22810:2010, часы подходят для любительского дайвинга до 40 м, защищены "
             "от пыли по IP6X и прошли испытания по MIL-STD 810H. Для навигации есть двухчастотный GPS и компас. "
             "Для настройки нужен iPhone 11 или новее с iOS 27.",
             "Прошлое поколение — {link_apple_watch_ultra_3}."],
            ["Ремешки и браслеты в наличии: {colors}."],
        ],
        "faq": [
            ("Чем Apple Watch Ultra 4 отличаются от Ultra 3?",
             ["Ultra 4 получили чип S11 вместо S10, новые датчики сердца и более ёмкую батарею: до 50 часов работы "
              "против 42 у Ultra 3 и до 84 часов в режиме энергосбережения против 72. Размер корпуса, размер и яркость экрана, "
              "защита от воды остались прежними."]),
            ("Можно ли нырять с Apple Watch Ultra 4?",
             ["Да, часы рассчитаны на любительский дайвинг до 40 м по стандарту EN13319: есть глубиномер и датчик "
              "температуры воды. Глубже 40 м Apple использовать их не рекомендует."]),
            ("Какие ремешки и браслеты есть в наличии?",
             ["Сейчас в наличии: {colors}.", "Размер ремешка указан в названии каждого товара."]),
        ],
    },
}


# ---------------------------------------------------------------- подборки
# Текст подборки /catalog/<slug>/ (seo.page_group) — после сетки товаров. Те же правила, что у MODELS: фрагмент
# выпадает, если в нём есть ссылка на модель без наличия ({link_…} пуст); {guide}, {guide_17_18}, {guide_which} — статьи.
COLLECTION_TEXTS = {
    "iphone": {
        "h2": "Как выбрать iPhone",
        "paras": [
            ["В каталоге ATOMM — iPhone нескольких поколений.",
             "Самые новые — {link_apple_iphone_18_pro} и {link_apple_iphone_18_pro_max} на чипе A20 Pro.",
             "Линейка 2025 года — {link_apple_iphone_17}, {link_apple_iphone_17_pro}, {link_apple_iphone_17_pro_max} "
             "и тонкий лёгкий {link_apple_iphone_air}.",
             "В марте 2026 года к ней добавился доступный {link_apple_iphone_17e}.",
             "Модели 2024 года — {link_apple_iphone_16}, {link_apple_iphone_16_plus}, {link_apple_iphone_16_pro} "
             "и {link_apple_iphone_16_pro_max}."],
            ["Выбирая среди этих моделей, начните с размера экрана: 6,1 дюйма — у iPhone 16 и 17e, 6,3 дюйма — у iPhone 17 и Pro-моделей без приставки "
             "Max, 6,5 дюйма — у Air, 6,7 дюйма — у 16 Plus, 6,9 дюйма — у Pro Max. Затем решите, какая нужна камера: "
             "телефото с 4- или 5-кратным оптическим приближением есть только у Pro, у iPhone 16, 16 Plus и 17 "
             "сзади две камеры — основная и сверхширокоугольная, у Air и 17e — одна. Плавный экран ProMotion до 120 Гц "
             "есть у iPhone 17, Air и Pro, у iPhone 16, 16 Plus и 17e — 60 Гц. Дольше всех без розетки "
             "работают Pro Max: по данным Apple, 18 Pro Max воспроизводит видео до 43–45 часов в зависимости от типа SIM."],
            ["Обратите внимание на тип SIM: у многих моделей есть версии с лотком для nano-SIM и версии "
             "только с eSIM, а iPhone Air работает только с eSIM.",
             "Подробное сравнение линеек — в статье {guide_which}.",
             "Если выбираете размер флагмана, загляните в {guide}, а если сомневаетесь, стоит ли переходить "
             "на новое поколение Pro Max, — в {guide_17_18}."],
        ],
    },
    "samsung-galaxy": {
        "h2": "Какие Samsung Galaxy есть в ATOMM",
        "paras": [
            ["Флагман серии S — {link_samsung_galaxy_s26_ultra}: экран 6,9 дюйма, основная камера 200 Мп и перо S Pen, "
             "которое хранится в корпусе.",
             "Предыдущее поколение — {link_samsung_galaxy_s25_ultra} с тем же размером экрана 6,9 дюйма и аккумулятором "
             "5000 мА·ч.",
             "{link_samsung_galaxy_s26_fe} — версия серии S для тех, кому не нужен флагман за полную цену."],
            ["Складные смартфоны линейки Z Fold открываются как книжка: в разложенном виде это большой экран для работы, "
             "чтения и видео.",
             "Сейчас в каталоге — {link_samsung_galaxy_z_fold8} и {link_samsung_galaxy_z_fold8_ultra}.",
             "{link_samsung_galaxy_z_flip8} складывается пополам, как раскладушка, — в сложенном виде "
             "он заметно компактнее обычного смартфона."],
            ["Если нужен смартфон на каждый день без переплаты, посмотрите серию A — например, {link_samsung_galaxy_a56}.",
             "Базовые Galaxy S26 и S26+, другие модели серии A и прошлых поколений собраны на странице "
             "{link_telefony_samsung}.",
             "Все варианты по памяти и цвету — на странице каждой модели."],
        ],
    },
    "mac": {
        "h2": "Какой Mac выбрать",
        "paras": [
            ["В ATOMM — ноутбуки и настольные компьютеры Apple.",
             "Самые мощные ноутбуки в каталоге — {link_apple_macbook_pro_m5_14_16}: версии 14 и 16 дюймов на M5 Pro "
             "и M5 Max с тремя портами Thunderbolt 5 и памятью до 128 ГБ у M5 Max. Есть и базовая 14-дюймовая модель "
             "на M5, а из прошлого поколения — {link_apple_macbook_pro_m4_14_16}."],
            ["MacBook Air подойдёт тем, кому важны лёгкость и тишина: вентилятора в нём нет. Версии на M5 вышли в марте "
             "2026 года с экраном 13 и 15 дюймов; по данным Apple, они работают до 18 часов, а накопитель начинается "
             "с 512 ГБ.",
             "Смотрите {link_apple_macbook_air_m5_13_6} и {link_apple_macbook_air_m5_15}.",
             "Если ноутбук нужен для учёбы и повседневных задач, присмотритесь к MacBook Neo 2026 года: экран 13 дюймов, "
             "чип A18 Pro, вес 1,23 кг и, по данным Apple, до 16 часов потокового видео.",
             "MacBook Neo и MacBook в расширенных конфигурациях — на страницах {link_noutbuki_apple_macbook} "
             "и {link_kastomnye_apple_macbook}."],
            ["Для дома и офиса — компактный настольный {link_apple_mac_mini}; моноблоки iMac с экраном 24 дюйма "
             "Retina 4.5K собраны на странице {link_monobloki_apple_imac}.",
             "Мониторы Studio Display — в разделе {link_monitory_apple}.",
             "Чип, объём памяти и накопителя указаны в названии каждого товара, а все конфигурации — на странице модели."],
        ],
    },
    "ipad": {
        "h2": "Какой iPad выбрать",
        "paras": [
            ["В каталоге ATOMM — iPad разных линеек и поколений.",
             "Самые мощные — {link_apple_ipad_pro_11_m5_2025} и {link_apple_ipad_pro_13_m5_2025} на чипе M5, с экраном "
             "Ultra Retina XDR и Face ID.",
             "Золотая середина — iPad Air 2026 года на M4 с 12 ГБ памяти и Wi-Fi 7: {link_apple_ipad_air_11_2026} "
             "и {link_apple_ipad_air_13_2026}.",
             "Прошлое поколение Air на M3 — {link_apple_ipad_air_11_2025} и {link_apple_ipad_air_13_2025}."],
            ["Для учёбы, видео и чтения хватит базового {link_apple_ipad_11_2025} на чипе A16 с экраном 11 дюймов.",
             "Самый компактный — {link_apple_ipad_mini_2024} на A17 Pro с экраном 8,3 дюйма: его удобно держать одной "
             "рукой и брать в дорогу."],
            ["Выбирая iPad, начните с размера экрана: 8,3 дюйма у iPad mini (2024), 11 дюймов у базовой модели, 11 или 13 дюймов "
             "у Air и Pro. Затем решите, нужна ли мобильная связь: версия Wi-Fi + Cellular выходит в интернет без "
             "телефона, но тип SIM зависит от модели — например, iPad Air на M4 работает только с eSIM.",
             "Объём памяти, связь и цвет указаны в названии каждого товара, а у популярных моделей есть отдельные "
             "страницы по памяти."],
        ],
    },
    "airpods": {
        "h2": "Какие AirPods выбрать",
        "paras": [
            ["В ATOMM — основные линейки наушников Apple.",
             "Самые новые вкладыши — {link_airpods_5}: они вышли в сентябре 2026 года, и, по данным Apple, их активное "
             "шумоподавление убирает до 50% больше шума, чем у AirPods 4 с шумоподавлением. Версия с кейсом беспроводной "
             "зарядки играет до 5 часов с включённым шумоподавлением и до 22 часов с подзарядкой от кейса, а сам кейс "
             "заряжается по USB-C, от Qi-совместимых зарядок и от зарядки Apple Watch. У базовой версии — до 4 и до "
             "20 часов, кейс заряжается по USB-C."],
            ["Прошлое поколение вкладышей — {link_airpods_4} — бывает в двух версиях: обычной "
             "и с активным шумоподавлением.",
             "Чем они отличаются от AirPods 5, разобрали в статье {guide_airpods}.",
             "Другие модели — на странице {link_naushniki_apple}.",
             "Внутриканальные {link_airpods_pro_3} с амбушюрами лучше изолируют от шума и подойдут для метро, перелётов "
             "и спорта."],
            ["Полноразмерные {link_airpods_max_2} вышли в марте 2026 года на чипе H2: по данным Apple, шумоподавление у "
             "них до 1,5 раза эффективнее, чем у прошлого поколения, а работают они до 20 часов. Через кабель USB-C "
             "наушники воспроизводят звук без потерь.",
             "Если модель бывает в нескольких цветах, цвет указан в названии товара.",
             "Чехлы, амбушюры и другие аксессуары — на странице {link_aksessuary_dlya_apple_airpods}."],
        ],
    },
    "apple-watch": {
        "h2": "Какие Apple Watch выбрать",
        "paras": [
            ["В каталоге ATOMM — Apple Watch нескольких линеек.",
             "Самые новые часы — {link_apple_watch_ultra_4} и {link_apple_watch_series_12}, представленные "
             "в сентябре 2026 года.",
             "У Ultra 4, по данным Apple, новый чип S11, переработанные датчики пульса и ЭКГ и батарея, которой "
             "хватает примерно на два дня, а тренировка с GPS записывается до 18 часов."],
            ["Ultra — часы для спорта и путешествий: корпус 49 мм из титана, чёрного или натурального цвета, "
             "ремешки Alpine, Trail, Ocean и миланский браслет.",
             "Прошлое поколение — {link_apple_watch_ultra_3} — обычно стоит дешевле."],
            ["Series — универсальные часы на каждый день: корпус 42 или 46 мм, алюминиевый или титановый.",
             "Кроме новой Series 12, в каталоге есть {link_apple_watch_series_11}.",
             "Самые доступные — Apple Watch SE с корпусом 40 или 44 мм; их и другие модели ищите на странице "
             "{link_chasy_apple_watch}.",
             "Размер корпуса, материал, цвет и ремешок можно сравнить прямо в списке товаров выше.",
             "Учтите, что для настройки Apple Watch нужен iPhone."],
        ],
    },
    "dyson": {
        "h2": "Какая техника Dyson есть в ATOMM",
        "paras": [
            ["В каталоге — техника Dyson для ухода за волосами, уборки и климата в доме.",
             "Стайлеры Airwrap укладывают и завивают волосы потоком воздуха; есть комплектации для прямых и для "
             "кудрявых волос.",
             "Фены Supersonic, выпрямители Airstrait и Corrale тоже в каталоге; часть стайлеров собрана на странице "
             "{link_staylery_dyson}."],
            ["Беспроводные пылесосы — от V8 и V10 до V12 Detect Slim, V15 Detect, V16 Piston Animal и Gen5 Detect; "
             "есть тонкие PencilVac и моющие пылесосы Wash.",
             "Для тех, кому удобнее проводная модель, — пылесосы Big Ball с контейнером вместо мешка.",
             "У V15 Detect лазерная насадка подсвечивает на полу мелкую пыль, которую плохо видно глазом.",
             "Многие из пылесосов — на странице {link_pylesosy_dyson}.",
             "Для них есть фильтры, насадки, аккумуляторы и подставки: в названии аксессуара указано, к каким моделям "
             "он подходит."],
            ["Очистители воздуха Dyson Purifier и модели Purifier Humidify+Cool, которые ещё и увлажняют воздух, "
             "подойдут для квартиры и офиса.",
             "Если в названии товара есть пометка «Вилка EU», у него европейская вилка — она подходит к обычным "
             "розеткам в России.",
             "Модель и комплектацию проверяйте по карточке товара."],
        ],
    },
    "playstation": {
        "h2": "Какую PlayStation 5 выбрать",
        "paras": [
            ["В ATOMM — новые консоли Sony PlayStation 5 в версиях Slim и Pro.",
             "PlayStation 5 Slim бывает с дисководом и без него — версия Digital Edition, "
             "рассчитанная на цифровые игры.",
             "Версия с дисководом запускает и игры на дисках.",
             "В каталоге есть Slim с SSD на 825 ГБ и на 1 ТБ."],
            ["PlayStation 5 Pro — самая мощная консоль Sony с SSD на 2 ТБ: она рассчитана на игры в высоком "
             "разрешении на телевизорах 4K.",
             "По данным Sony, у неё более мощная графика, улучшенная трассировка лучей и масштабирование изображения "
             "PSSR.",
             "Встроенного дисковода у PS5 Pro нет — его можно докупить отдельно.",
             "Игры для PS5 работают и на Slim, и на Pro; игры на дисках на Digital Edition и Pro запускаются только "
             "с подключённым дисководом."],
            ["Объём памяти и версия консоли указаны в названии каждого товара.",
             "В комплекте с консолью один геймпад DualSense: чтобы играть вдвоём, понадобится второй.",
             "Геймпады — на странице {link_besprovodnye_igrovye_kontrollery}, игры — на странице "
             "{link_igry_dlya_pristavok}."],
        ],
    },
}


# ---------------------------------------------------------------- статьи
# Статья рендерится в seo.page_guide(); {lo_1}, {lo_2} (цены моделей из "models" по порядку), {colors_1}, {colors_2},
# {colors_sentence} подставляются из каталога,
# блок «Где посмотреть варианты» со ссылками на модели и страницы памяти строится там же (только для существующих страниц).
GUIDES = {
    "iphone-18-pro-vs-18-pro-max": {
        "title": "iPhone 18 Pro или 18 Pro Max: в чём разница и что выбрать",
        "seo_title": "iPhone 18 Pro или 18 Pro Max: в чём разница и что выбрать | ATOMM",
        "desc": "Сравнение iPhone 18 Pro и 18 Pro Max по официальным характеристикам Apple: экран, вес, батарея, "
                "eSIM и nano-SIM. Что одинаковое, чем отличаются и кому какая модель подойдёт.",
        "published": "2026-11-10",
        "modified": "2026-11-10",
        "models": ("apple-iphone-18-pro", "apple-iphone-18-pro-max"),
        "sources": SOURCES["iphone-18-pro"],
        "body": """
<p>iPhone 18 Pro и 18 Pro Max — Pro-модели этого года. Внутри они почти одинаковые, поэтому выбор сводится к трём вещам:
размеру экрана, весу и времени работы от батареи. Разбираем по официальным характеристикам Apple.</p>

<h2>Что у моделей одинаковое</h2>
<p>Обе модели работают на чипе A20 Pro. Камеры тоже общие: основная 48 Мп (24 мм) с переменной диафрагмой ƒ/1.48–ƒ/4.0,
сверхширокоугольная 48 Мп (13 мм, угол обзора 120°) и телефото 48 Мп (100 мм) с 4-кратным приближением. В режиме 8× телефон
снимает 12-мегапиксельные кадры оптического качества, цифровой зум — до 40×. Фронтальная камера — 18 Мп с Center Stage.</p>
<p>Экраны сделаны по одной технологии: Super Retina XDR OLED с плотностью 460 ppi, ProMotion до 120 Гц, яркость до 1600 нит
в HDR и до 3000 нит на улице. Совпадают корпус (алюминиевый unibody, Ceramic Shield 2 спереди), защита IP68 (до 6 м
в течение 30 минут), разъём USB-C со скоростью USB 3 до 10 Гбит/с и кнопка Camera Control. Объёмы памяти одинаковые — 256 ГБ,
512 ГБ, 1 ТБ и 2 ТБ, цвета тоже.{colors_sentence}</p>

<h2>Чем отличаются</h2>
<table class="cmp">
<tr><th></th><th>iPhone 18 Pro</th><th>iPhone 18 Pro Max</th></tr>
<tr><td>Экран</td><td>6,3″, 2622×1206</td><td>6,9″, 2868×1320</td></tr>
<tr><td>Размеры</td><td>150,0×71,9×8,75 мм</td><td>163,4×78,0×8,75 мм</td></tr>
<tr><td>Вес</td><td>211 г</td><td>249 г</td></tr>
<tr><td>Видео, версия только с eSIM</td><td>до 36 ч</td><td>до 45 ч</td></tr>
<tr><td>Видео, версия с nano-SIM</td><td>до 34 ч</td><td>до 43 ч</td></tr>
<tr><td>Цена в ATOMM</td><td>{lo_1}</td><td>{lo_2}</td></tr>
</table>
<p>Толщина у обеих моделей одинаковая — 8,75 мм. Pro Max выше на 13,4 мм, шире на 6,1 мм и тяжелее на 38 г.</p>

<h2>Батарея, eSIM и nano-SIM</h2>
<p>Разница в автономности — главное практическое отличие: по данным Apple, Pro Max воспроизводит видео на 9 часов дольше.
Есть и второй нюанс — тип SIM. Версия только с eSIM не имеет лотка для SIM-карты и, по данным Apple, работает дольше
версии с nano-SIM: на 2 часа у обеих моделей. Одновременно работают две eSIM. Если вы хотите вставить обычную
SIM-карту, нужна версия Nano SIM + eSIM; если готовы перейти на eSIM, заранее уточните у оператора, выдаёт ли он её.
Тип SIM указан в названии каждого товара в каталоге.</p>

<h2>Что выбрать</h2>
<p><b>iPhone 18 Pro</b> подойдёт, если телефон должен быть компактным: им удобнее пользоваться одной рукой, он заметно легче. При этом вы ничего не теряете в камерах и производительности — они такие же, как у старшей модели.</p>
<p><b>iPhone 18 Pro Max</b> стоит брать, если вы много смотрите видео, играете или читаете с телефона и редко бываете
рядом с розеткой: больший экран и запас в 9 часов видео заметны каждый день. Цена этого — лишние 38 г и размер,
с которым не всем удобно.</p>
<p>Если сомневаетесь, отталкивайтесь от того, каким телефоном пользуетесь сейчас: экран 6,3 дюйма — как у iPhone 17
и 17 Pro, 6,9 дюйма — как у 17 Pro Max.</p>

""",
    },
    "iphone-17-pro-max-vs-18-pro-max": {
        "title": "iPhone 17 Pro Max или 18 Pro Max: в чём разница и что выбрать",
        "seo_title": "iPhone 17 Pro Max или 18 Pro Max: сравнение и что выбрать | ATOMM",
        "desc": "Сравнение iPhone 17 Pro Max и 18 Pro Max по официальным характеристикам Apple: чип, камера, батарея, "
                "вес, eSIM и nano-SIM. Что изменилось в новинке и кому хватит прошлой модели.",
        "published": "2026-11-12",
        "modified": "2026-11-12",
        "models": ("apple-iphone-17-pro-max", "apple-iphone-18-pro-max"),
        "sources": SOURCES["iphone-17-18-pro-max"],
        "body": """
<p>iPhone 18 Pro Max внешне почти не отличается от 17 Pro Max: тот же размер, тот же экран, та же компоновка камер.
Разница — в чипе, основной камере и батарее. Разбираем по официальным
характеристикам Apple, что изменилось и за что вы доплачиваете.</p>

<h2>Что у моделей одинаковое</h2>
<p>Экран — Super Retina XDR OLED 6,9 дюйма, 2868×1320 точек, 460 ppi, ProMotion до 120 Гц, до 1600 нит в HDR и до 3000 нит
на улице. Габариты совпадают до миллиметра: 163,4×78,0×8,75 мм. Корпус в обоих случаях — алюминиевый unibody с Ceramic Shield 2
спереди, защита IP68, разъём USB-C со скоростью USB 3 до 10 Гбит/с, кнопка Camera Control.</p>
<p>Сверхширокоугольная камера (48 Мп, 13 мм) и телефото (48 Мп, 100 мм, 4-кратное приближение, режим 8× с 12-мегапиксельными
кадрами оптического качества) у моделей одинаковые, как и фронтальная камера 18 Мп с Center Stage. Объёмы памяти тоже
совпадают — 256 ГБ, 512 ГБ, 1 ТБ и 2 ТБ.</p>

<h2>Чем отличаются</h2>
<table class="cmp">
<tr><th></th><th>iPhone 17 Pro Max</th><th>iPhone 18 Pro Max</th></tr>
<tr><td>Чип</td><td>A19 Pro</td><td>A20 Pro</td></tr>
<tr><td>Основная камера</td><td>48 Мп, ƒ/1.78</td><td>48 Мп, диафрагма ƒ/1.48, ƒ/1.8, ƒ/2.8 или ƒ/4.0</td></tr>
<tr><td>Видео, версия только с eSIM</td><td>до 39 ч</td><td>до 45 ч</td></tr>
<tr><td>Видео, версия с nano-SIM</td><td>до 37 ч</td><td>до 43 ч</td></tr>
<tr><td>Вес</td><td>231 г (nano-SIM), 233 г (eSIM)</td><td>249 г</td></tr>
<tr><td>Цвета в ATOMM</td><td>{colors_1}</td><td>{colors_2}</td></tr>
<tr><td>Цена в ATOMM</td><td>{lo_1}</td><td>{lo_2}</td></tr>
</table>
<p>Ещё одно отличие — связь: в 18 Pro Max стоит собственный модем Apple C2. Палитры у поколений почти не пересекаются —
общий только серебристый цвет, так что, если вам нравится конкретный оттенок, это может решить выбор само по себе.</p>

<h2>Камера: что даёт переменная диафрагма</h2>
<p>У 17 Pro Max диафрагма основной камеры фиксированная — ƒ/1.78. У 18 Pro Max она переключается между четырьмя значениями — ƒ/1.48, ƒ/1.8, ƒ/2.8 и ƒ/4.0.
Самое открытое значение пропускает больше света — это помогает при съёмке в темноте. Прикрытая диафрагма увеличивает
глубину резкости: в кадре остаётся чётким больше планов, например при съёмке группы людей или пейзажа с передним планом.
Остальные камеры у моделей одинаковые, поэтому разницу заметят в первую очередь те, кто много снимает на основную камеру.</p>

<h2>Батарея и вес</h2>
<p>По данным Apple, 18 Pro Max воспроизводит видео на 6 часов дольше 17 Pro Max — и в версии только с eSIM (45 ч против 39),
и в версии с nano-SIM (43 ч против 37). Плата за это — вес: новинка тяжелее на 16–18 г в зависимости от версии.
При одинаковых размерах разница ощущается в руке.</p>
<p>Версия только с eSIM у обеих моделей работает дольше, но в ней нет лотка для SIM-карты. Если пользуетесь обычной
SIM-картой, выбирайте версию Nano SIM + eSIM; тип SIM указан в названии каждого товара в каталоге.</p>

<h2>Что выбрать</h2>
<p><b>iPhone 18 Pro Max</b> стоит брать, если важны максимальная автономность и камера для съёмки в сложном свете,
а телефон вы покупаете на несколько лет и хотите самое новое поколение.</p>
<p><b>iPhone 17 Pro Max</b> — разумный выбор, если нужен большой экран и три камеры по 48 Мп за меньшие деньги: экран,
размеры, телефото и сверхширокоугольная камера у него такие же, а сам телефон легче. 37–39 часов видео большинству
хватает с запасом на день.</p>
<p>Если у вас уже 17 Pro Max, переход на 18 Pro Max оправдан в первую очередь ради батареи и основной камеры — экран
и габариты останутся прежними. Если выбираете между размерами внутри нового поколения, загляните в сравнение
<a href="/guides/iphone-18-pro-vs-18-pro-max/">iPhone 18 Pro и 18 Pro Max</a>.</p>
""",
    },
    # {link_<slug>} — ссылка на страницу модели, если она в наличии, иначе просто название (seo.page_guide);
    # "grids": False — без сеток товаров по каждой модели (моделей в статье много, ссылки — в «Где посмотреть варианты»)
    "kakoy-iphone-kupit-2026": {
        "title": "Какой iPhone купить в 2026 году: сравнение моделей",
        "seo_title": "Какой iPhone купить в 2026 году: сравнение линеек и цены | ATOMM",
        "desc": "Какой айфон выбрать в 2026 году: iPhone 18 Pro, 17, Air, 17e и 16 — сравнение по экрану, камерам, "
                "батарее и весу по официальным данным Apple. Кому какая модель подойдёт.",
        "published": "2026-11-13",
        "modified": "2026-11-13",
        "models": ("apple-iphone-18-pro-max", "apple-iphone-18-pro", "apple-iphone-17-pro-max", "apple-iphone-17-pro",
                   "apple-iphone-air", "apple-iphone-17", "apple-iphone-17e", "apple-iphone-16-pro-max",
                   "apple-iphone-16-pro", "apple-iphone-16-plus", "apple-iphone-16"),
        "grids": False,
        # {older} — абзац «вводная фраза + ссылки» на модели вне таблицы: только модели в наличии, нет ни одной — абзаца нет
        "more_models": {"older": ("Кроме моделей из таблицы, в каталоге есть и другие iPhone:",
                                  ("apple-iphone-16e", "apple-iphone-15", "apple-iphone-15-plus", "apple-iphone-15-pro",
                                   "apple-iphone-15-pro-max", "apple-iphone-14"),
                                  ". Цены и все варианты — на страницах моделей.")},
        "sources": (SOURCES["iphone-17-18-pro-max"][2:4] + SOURCES["iphone-17-pro"][1:3] + SOURCES["iphone-17-18-pro-max"][:2]
                    + SOURCES["iphone-air-specs"] + SOURCES["iphone-17-specs"] + SOURCES["iphone-17e"][:1]
                    + SOURCES["iphone-16-pro"][:1] + SOURCES["iphone-16-pro-max"] + SOURCES["iphone-16-plus"][:1]
                    + SOURCES["iphone-16"][:1] + SOURCES["iphone-16"][2:] + SOURCES["iphone-17e"][3:]
                    + ["https://9to5mac.com/2026/09/09/no-iphone-18-announced-today-heres-why/"]),
        "body": """
<p>В 2026 году в продаже сразу три поколения iPhone: Pro-модели этого года, линейка 2025 года с весенним iPhone 17e
и модели 2024 года. Цены у них заметно отличаются, а разница в характеристиках не всегда очевидна. Сравниваем
основные модели трёх последних поколений из каталога ATOMM по официальным данным Apple. В сентябре 2026 года Apple
представила iPhone 18 Pro, 18 Pro Max и складной iPhone Duo, а базовый iPhone 18 не показала — по сообщениям СМИ,
его ждут в начале 2027 года, поэтому в сравнении его нет.</p>

<h2>Сравнение моделей</h2>
<table class="cmp">
<tr><th>Модель</th><th>Экран</th><th>Чип</th><th>Камеры сзади</th><th>Видео, до</th><th>Вес</th><th>Цена в ATOMM</th></tr>
<tr><td>{link_apple_iphone_18_pro_max}</td><td>6,9″, 120 Гц</td><td>A20 Pro</td><td>3 × 48 Мп</td><td>43–45 ч</td><td>249 г</td><td>{lo_1}</td></tr>
<tr><td>{link_apple_iphone_18_pro}</td><td>6,3″, 120 Гц</td><td>A20 Pro</td><td>3 × 48 Мп</td><td>34–36 ч</td><td>211 г</td><td>{lo_2}</td></tr>
<tr><td>{link_apple_iphone_17_pro_max}</td><td>6,9″, 120 Гц</td><td>A19 Pro</td><td>3 × 48 Мп</td><td>37–39 ч</td><td>231–233 г</td><td>{lo_3}</td></tr>
<tr><td>{link_apple_iphone_17_pro}</td><td>6,3″, 120 Гц</td><td>A19 Pro</td><td>3 × 48 Мп</td><td>31–33 ч</td><td>204–206 г</td><td>{lo_4}</td></tr>
<tr><td>{link_apple_iphone_air}</td><td>6,5″, 120 Гц</td><td>A19 Pro</td><td>48 Мп</td><td>27 ч</td><td>165 г</td><td>{lo_5}</td></tr>
<tr><td>{link_apple_iphone_17}</td><td>6,3″, 120 Гц</td><td>A19</td><td>2 × 48 Мп</td><td>30 ч</td><td>177 г</td><td>{lo_6}</td></tr>
<tr><td>{link_apple_iphone_17e}</td><td>6,1″, 60 Гц</td><td>A19</td><td>48 Мп</td><td>26 ч</td><td>170 г</td><td>{lo_7}</td></tr>
<tr><td>{link_apple_iphone_16_pro_max}</td><td>6,9″, 120 Гц</td><td>A18 Pro</td><td>48 + 48 + 12 Мп</td><td>33 ч</td><td>227 г</td><td>{lo_8}</td></tr>
<tr><td>{link_apple_iphone_16_pro}</td><td>6,3″, 120 Гц</td><td>A18 Pro</td><td>48 + 48 + 12 Мп</td><td>27 ч</td><td>199 г</td><td>{lo_9}</td></tr>
<tr><td>{link_apple_iphone_16_plus}</td><td>6,7″, 60 Гц</td><td>A18</td><td>48 + 12 Мп</td><td>27 ч</td><td>199 г</td><td>{lo_10}</td></tr>
<tr><td>{link_apple_iphone_16}</td><td>6,1″, 60 Гц</td><td>A18</td><td>48 + 12 Мп</td><td>22 ч</td><td>170 г</td><td>{lo_11}</td></tr>
</table>
<p>Время работы — воспроизведение видео по данным Apple. Там, где указан диапазон, меньшее значение относится к версии
с лотком для nano-SIM, большее — к версии только с eSIM; так же и с весом 17 Pro и 17 Pro Max. Цена — минимальная
за модель в наличии, она зависит от памяти, цвета и типа SIM.</p>

<h2>Pro-модели: если важны камера и батарея</h2>
<p>У всех Pro-моделей есть телефото-камера. У 17 Pro, 17 Pro Max, 18 Pro и 18 Pro Max все три камеры по 48 Мп,
а телефото даёт 4-кратное оптическое приближение. У 16 Pro и 16 Pro Max телефото 12 Мп, но с 5-кратным приближением.
В 18 Pro и 18 Pro Max основная камера получила переменную диафрагму — от ƒ/1.48 до ƒ/4.0, а внутри у них
новый чип A20 Pro. Самый большой запас батареи в таблице — у 18 Pro Max.
Корпус Pro-моделей 2025 и 2026 годов — алюминиевый, у 16 Pro и 16 Pro Max — титановый.</p>
<p>Внутри одного поколения Pro и Pro Max различаются только размером, весом и батареей — подробнее в статье
<a href="/guides/iphone-18-pro-vs-18-pro-max/">«iPhone 18 Pro или 18 Pro Max»</a>. Если выбираете между поколениями
Pro Max, загляните в сравнение <a href="/guides/iphone-17-pro-max-vs-18-pro-max/">«iPhone 17 Pro Max или 18 Pro Max»</a>.
Если модель уже выбрана и осталось определиться с объёмом, читайте, <a href="/guides/iphone-18-pro-max-skolko-pamyati/">сколько
памяти брать в iPhone 18 Pro Max</a>.</p>

<h2>iPhone 17 и iPhone Air: середина линейки</h2>
<p><b>iPhone 17</b> — самый сбалансированный вариант без приставки Pro: экран 6,3 дюйма с ProMotion до 120 Гц, как у
Pro-моделей, чип A19, две камеры по 48 Мп — основная и сверхширокоугольная — и до 30 часов видео. Телефото нет, но для
повседневной съёмки это редко критично. Память начинается с 256 ГБ.</p>
<p><b>iPhone Air</b> выбирают за корпус: толщина 5,64 мм и вес 165 г — это самый лёгкий iPhone в таблице. Внутри
чип A19 Pro, экран 6,5 дюйма с ProMotion. Компромиссы — одна задняя камера, до 27 часов видео и только eSIM:
лотка для SIM-карты нет ни в одной версии.</p>

<h2>Доступные модели: iPhone 17e, 16 и 16 Plus</h2>
<p><b>iPhone 17e</b> — самый новый из доступных iPhone: чип A19, как у iPhone 17, одна камера 48 Мп с 2-кратным
приближением оптического качества, экран 6,1 дюйма на 60 Гц и до 26 часов видео. Минимальный объём памяти — 256 ГБ.</p>
<p><b>iPhone 16</b> и <b>16 Plus</b> — модели 2024 года на чипе A18 с двумя камерами: основной 48 Мп
и сверхширокоугольной 12 Мп. У обеих есть кнопки Action и Camera Control, экран на 60 Гц. 16 Plus крупнее —
экран 6,7 дюйма — и, по данным Apple, держит заряд на 5 часов дольше, но весит почти на 30 г больше. Если нужен
большой экран без доплаты за Pro, присмотритесь к 16 Plus.</p>
{older}

<h2>Что выбрать</h2>
<p><b>Нужны камеры нового поколения и максимум автономности</b> — 18 Pro Max; те же камеры в компактном корпусе,
но с батареей поменьше — 18 Pro. Сэкономить
без отказа от телефото и трёх камер по 48 Мп можно с 17 Pro и 17 Pro Max.</p>
<p><b>Нужен быстрый iPhone с плавным экраном, но без переплаты за Pro</b> — iPhone 17.</p>
<p><b>Важны лёгкость и тонкий корпус</b> — iPhone Air, если вас устраивают одна камера и eSIM.</p>
<p><b>Нужен iPhone подешевле</b> — из моделей в таблице это 17e с новым чипом A19 и iPhone 16, с большим экраном —
16 Plus.</p>
<p>Тип SIM указан в названии каждого товара в каталоге: если пользуетесь обычной SIM-картой, выбирайте версию
Nano SIM + eSIM, а перед покупкой версии только с eSIM уточните у оператора, выдаёт ли он eSIM.</p>
""",
    },
    "iphone-18-pro-max-esim-ili-nano-sim": {
        "title": "iPhone 18 Pro Max только с eSIM или с nano-SIM: какую версию выбрать",
        "seo_title": "iPhone 18 Pro Max только с eSIM или с nano-SIM: какую версию выбрать | ATOMM",
        "desc": "Чем версия iPhone 18 Pro Max только с eSIM отличается от версии с nano-SIM, в каких странах какая "
                "продаётся, какой номер модели у европейской версии и как его проверить. Что выбрать в России.",
        "published": "2026-11-14",
        "modified": "2026-11-14",
        "models": ("apple-iphone-18-pro-max", "apple-iphone-18-pro"),
        "sources": SOURCES["iphone-18-sim"],
        "body": """
<p>iPhone 18 Pro Max, как и 18 Pro, выпускается в двух версиях: с лотком для nano-SIM и поддержкой eSIM или только
с eSIM, без лотка. Какая версия у телефона, зависит от страны, для которой он выпущен. Разбираем по данным Apple,
чем версии отличаются, как узнать свою и какую выбрать, если пользоваться телефоном вы будете в России.</p>

<h2>Какая версия где продаётся</h2>
<table class="cmp">
<tr><th>Страны и регионы</th><th>SIM</th><th>18 Pro Max</th><th>18 Pro</th></tr>
<tr><td>США, Пуэрто-Рико</td><td>только eSIM</td><td>A3473</td><td>A3472</td></tr>
<tr><td>Канада, Мексика, Япония, Гуам, Виргинские острова (США), Бахрейн, Катар, Кувейт, ОАЭ, Оман, Саудовская Аравия</td>
<td>только eSIM</td><td>A3716</td><td>A3713</td></tr>
<tr><td>Материковый Китай</td><td>nano-SIM или eSIM</td><td>A3718</td><td>A3715</td></tr>
<tr><td>Остальные страны и регионы, в том числе Европа</td><td>nano-SIM и eSIM</td><td>A3717</td><td>A3714</td></tr>
</table>
<p>Номера моделей и список стран — из справки Apple «Как определить модель iPhone». Европейская версия 18 Pro Max —
A3717, 18 Pro — A3714: в них есть лоток для nano-SIM на левой грани, а вторую линию можно подключить через eSIM
или использовать две eSIM. В версиях только с eSIM лотка нет, одновременно работают две eSIM, а сохранить
в телефоне можно восемь и больше.</p>

<h2>Чем версии отличаются</h2>
<p>Кроме способа подключить номер, различие одно — время работы. По данным Apple, версии только с eSIM
воспроизводят видео на 2 часа дольше. Вес у версий одинаковый: 249 г у 18 Pro Max и 211 г у 18 Pro.</p>
<table class="cmp">
<tr><th></th><th>iPhone 18 Pro Max</th><th>iPhone 18 Pro</th></tr>
<tr><td>Видео, версия только с eSIM</td><td>до 45 ч</td><td>до 36 ч</td></tr>
<tr><td>Видео, версия с nano-SIM</td><td>до 43 ч</td><td>до 34 ч</td></tr>
<tr><td>Цена в ATOMM</td><td>{lo_1}</td><td>{lo_2}</td></tr>
</table>

<h2>Как узнать, какая версия у вас</h2>
<p>Откройте «Настройки» → «Основные» → «Об этом устройстве». Справа от строки «Номер модели» показан номер детали;
нажмите на него — появится номер модели, который начинается с буквы A, например A3717. Сравните его с таблицей выше.
У версии с лотком номер модели также нанесён внутри слота для SIM-карты: его видно, если извлечь лоток. В каталоге ATOMM
тип SIM указан в названии каждого товара.</p>

<h2>Что работает в России</h2>
<p>В версию с nano-SIM можно вставить обычную SIM-карту российского оператора. Для версии
только с eSIM номер нужно перевести на eSIM. По данным iPhones.ru, eSIM выдают МТС, Билайн, МегаФон и T2, в том числе
дистанционно: на сайте или в приложении оператора, с подтверждением личности через Госуслуги. Профиль добавляется
в разделе «Настройки» → «Сотовая связь» → «Добавить eSIM», обычно по QR-коду. Условия у операторов отличаются, поэтому
перед покупкой eSIM-версии уточните у своего, выдаёт ли он eSIM на ваш тариф.</p>

<h2>Что выбрать</h2>
<p><b>Версия с nano-SIM</b> подойдёт, если вы пользуетесь обычной SIM-картой и не хотите менять её на eSIM, часто
переставляете SIM-карту между телефонами или вставляете местную SIM-карту в поездках. eSIM в ней тоже работает.</p>
<p><b>Версия только с eSIM</b> — если вы уже перешли на eSIM или готовы это сделать: она немного дольше держит заряд,
но обычную SIM-карту в неё не вставить. Если выбираете не только SIM, но и размер, загляните в сравнение
<a href="/guides/iphone-18-pro-vs-18-pro-max/">«iPhone 18 Pro или 18 Pro Max»</a>. Все варианты по памяти
и цвету — на страницах {link_apple_iphone_18_pro_max} и {link_apple_iphone_18_pro}.</p>
""",
    },
    # "mem_guide": статья про выбор памяти одной модели. Хвост заголовка (": 256 ГБ, 512 ГБ или 1 ТБ"), таблица цен,
    # разделы и краткие итоги — только по объёмам в наличии (seo.mem_guide_ctx); в разделах {lo} — цена «от»
    # за этот объём, {mem} — ссылка на страницу памяти; "absent" — текст для объёма, которого нет в наличии.
    "iphone-18-pro-max-skolko-pamyati": {
        "title": "Сколько памяти брать в iPhone 18 Pro Max",
        "seo_title": "{title} | ATOMM",
        "desc": "Какой объём памяти iPhone 18 Pro Max выбрать: кому хватит базового, когда стоит доплатить за больший, "
                "сколько места занимает видео ProRes и чем поможет iCloud. Цены — по наличию.",
        "published": "2026-11-16",
        "modified": "2026-11-16",
        "models": ("apple-iphone-18-pro-max",),
        "sources": SOURCES["iphone-18-pro-max-memory"],
        "mem_guide": {
            "model": "apple-iphone-18-pro-max",
            "title_tail": ": {choice}",             # H1: полный список, только при ≥2 объёмах в наличии
            "seo_tail": ": от {lo} до {hi}",          # <title>: короткий хвост по min/max в наличии
            "all_mems": (256, 512, 1024, 2048),       # весь набор Apple: если в наличии все — {mem_intro} не выводим
            "neighbors": "Если сомневаетесь между двумя соседними объёмами, берите больший: расширить память потом "
                         "не получится. ",
            "intro": "Сейчас в ATOMM в наличии версии на {mems}.",
            "table_h2": "Цены по объёму памяти",
            "sections": {
                256: """<h2>256 ГБ — {lo}</h2>
<p>Базового объёма хватит, если вы снимаете фото и видео в стандартном формате HEVC, держите в телефоне мессенджеры,
соцсети, карты и пару игр, а фотоархив храните в iCloud или на компьютере. Это разумный выбор для тех, кто снимает
короткие ролики, а не часовые записи в 4K. Ориентир простой: если на нынешнем телефоне у вас занято больше 150–200 ГБ
и архив продолжает расти, 256 ГБ через год-два станет тесно. Все варианты — {mem}.</p>""",
                512: """<h2>512 ГБ — {lo}</h2>
<p>Самый спокойный вариант для тех, кто много снимает: поездки, детские праздники, видео для соцсетей в 4K. Запас
пригодится, если вы не хотите полностью зависеть от облака, скачиваете фильмы и музыку в дорогу или играете в большие
игры. Если планируете пользоваться телефоном три-четыре года и не готовы регулярно чистить галерею, начинайте
выбор с этого объёма. Все варианты — {mem}.</p>""",
                1024: """<h2>1 ТБ — {lo}</h2>
<p>Объём для тех, кто снимает всерьёз: в ProRes и Apple Log 2, с последующим монтажом и цветокоррекцией прямо
на телефоне. Такие ролики съедают свободное место за считаные съёмки, а с запасом в терабайт материал можно
спокойно держать в телефоне до конца монтажа. 1 ТБ подойдёт и тем, кто хочет носить с собой весь фото- и видеоархив
без облака. Все варианты — {mem}.</p>""",
                2048: """<h2>2 ТБ — {lo}</h2>
<p>Максимальный объём рассчитан на профессиональную съёмку: ProRes и ProRes RAW, длинные
съёмочные дни, когда нет возможности сбросить материал на компьютер. Для обычной съёмки, приложений и игр такой запас
избыточен — переплачивать за него имеет смысл, только если телефон работает как камера. Все варианты — {mem}.</p>""",
            },
            "absent": {
                2048: """<h2>2 ТБ</h2>
<p>Apple выпускает iPhone 18 Pro Max и на 2 ТБ — эта версия рассчитана на профессиональную съёмку в ProRes и ProRes RAW.
Сейчас в ATOMM её нет в наличии.</p>""",
            },
            "summary": {
                256: "<b>256 ГБ</b> ({lo}) — обычная съёмка, архив в iCloud или на компьютере.",
                512: "<b>512 ГБ</b> ({lo}) — много видео в 4K, офлайн-фильмы и игры, телефон на несколько лет.",
                1024: "<b>1 ТБ</b> ({lo}) — съёмка в ProRes и Apple Log 2, монтаж на телефоне, архив без облака.",
                2048: "<b>2 ТБ</b> ({lo}) — телефон как основная камера для профессиональной съёмки.",
            },
        },
        "body": """
<p>Память в iPhone 18 Pro Max выбирают один раз: слота для карты памяти нет, и после покупки объём не увеличить.
Apple выпускает модель в четырёх вариантах — от 256 ГБ до 2 ТБ. {mem_intro} Разбираем, кому какого
объёма хватит и когда доплата за больший действительно оправдана.</p>
{mem_table}

<h2>Сколько места реально свободно</h2>
<p>Заявленный объём — это не свободное место. По данным Apple, система и стандартные приложения занимают примерно
от 12 до 24 ГБ, так что на младшей версии пользователю остаётся меньше. Дальше всё решают фото и особенно видео:
iPhone 18 Pro Max снимает 4K Dolby Vision с частотой до 120 кадров/с, а профессиональные форматы занимают
в разы больше места. Apple прямо предупреждает, что файлы ProRes бывают до 30 раз больше видео в формате HEVC.</p>
<p>Есть и ограничения, которые зависят не от объёма. Во внутреннюю память ProRes записывается в 4K с частотой
до 30 кадров/с; для 4K при 60 и 120 кадрах/с Apple указывает требования к внешнему накопителю — скорость записи
от 220 и 440 МБ/с соответственно. То есть самые тяжёлые режимы рассчитаны на внешний SSD, какой бы объём памяти вы ни выбрали.</p>

{mem_sections}

<h2>Если места не хватает: iCloud и внешний диск</h2>
<p><b>iCloud.</b> Функция «Фото iCloud» хранит снимки и видео в облаке в исходном качестве. Если включить оптимизацию
хранилища, на телефоне остаются облегчённые копии, а оригиналы скачиваются по запросу — по Wi-Fi или через мобильную
сеть. Фото и видео при этом занимают место в iCloud, поэтому объём облака должен быть рассчитан на ваш архив.
Это хорошее дополнение к памяти телефона, но не замена памяти для тех, кто снимает в ProRes: такие файлы нужны
на телефоне целиком, пока вы их монтируете.</p>
<p><b>Внешний накопитель.</b> Порт USB-C в iPhone 18 Pro Max работает на скорости USB 3 — до 10 Гбит/с, нужен
кабель с такой же скоростью. Внешний SSD, отформатированный в exFAT, подходит для записи ProRes и для того, чтобы
быстро сбросить отснятое и освободить место.</p>

<h2>Коротко: какой объём выбрать</h2>
{mem_summary}
<p>{mem_neighbors}Остальное
у версий одинаковое — чип, камеры, экран и батарея не зависят от объёма. Тип SIM и цвет выбираются отдельно:
о версиях с eSIM и nano-SIM — в статье <a href="/guides/iphone-18-pro-max-esim-ili-nano-sim/">«iPhone 18 Pro Max только
с eSIM или с nano-SIM»</a>.</p>
""",
    },
    # тот же механизм "mem_guide", что у статьи про 18 Pro Max: хвост H1/title, таблица и разделы — по наличию
    "iphone-18-pro-skolko-pamyati": {
        "title": "iPhone 18 Pro: сколько памяти выбрать",
        "seo_title": "{title} | ATOMM",
        "desc": "Какой объём памяти iPhone 18 Pro выбрать — 256 ГБ, 512 ГБ, 1 ТБ или 2 ТБ: сколько места занимает "
                "система, видео 4K и ProRes, когда хватит базовой версии и кому нужен запас. Цены — по наличию.",
        "published": "2026-11-17",
        "modified": "2026-11-17",
        "models": ("apple-iphone-18-pro",),
        "sources": SOURCES["iphone-18-pro-memory"],
        "mem_guide": {
            "model": "apple-iphone-18-pro",
            "short_anchor": True,                    # в разделах анкор — «512 ГБ», а не «iPhone 18 Pro 512 ГБ»
            "title_tail": " — {choice}",
            "seo_tail": " — от {lo} до {hi}",
            "all_mems": (256, 512, 1024, 2048),
            "neighbors": "Не можете выбрать между двумя соседними объёмами — берите больший: докупить память "
                         "после покупки нельзя. ",
            "intro": "Сейчас в ATOMM в наличии версии на {mems}.",
            "table_h2": "Цены iPhone 18 Pro по объёму памяти",
            "sections": {
                256: """<h2>256 ГБ — {lo}</h2>
<p>Младшая версия рассчитана на тех, кто снимает в обычном режиме — фото и видео в HEVC, — пользуется мессенджерами,
картами, банковскими приложениями и не держит в телефоне большие игры. Хорошо работает в паре с «Фото iCloud»: оригиналы
уходят в облако, на телефоне остаются облегчённые копии. Проверьте, сколько места занято на нынешнем телефоне: если
больше 150 ГБ, через пару лет 256 ГБ может не хватить. Все версии на {mem}.</p>""",
                512: """<h2>512 ГБ — {lo}</h2>
<p>Золотая середина для тех, кто часто снимает видео в 4K, сохраняет фильмы и сериалы для поездок и не хочет
постоянно чистить галерею. Если телефон берётся на три года и больше, а подписку на облако расширять не хочется,
этот объём снимает вопрос со свободным местом. Все версии на {mem}.</p>""",
                1024: """<h2>1 ТБ — {lo}</h2>
<p>Версия для тех, кто снимает в ProRes или Apple Log 2 и монтирует ролики прямо на телефоне: исходники нужны
на устройстве целиком, и запас в терабайт позволяет не сбрасывать их после каждой съёмки. Подойдёт и тем, кто хочет
держать весь фото- и видеоархив под рукой без облака. Все версии на {mem}.</p>""",
                2048: """<h2>2 ТБ — {lo}</h2>
<p>Максимальный объём нужен, когда iPhone 18 Pro работает как основная камера: длинные съёмочные дни в ProRes
и ProRes RAW без возможности сбросить материал на компьютер. Для приложений, игр и обычной съёмки он избыточен.
Все версии на {mem}.</p>""",
            },
            "absent": {
                2048: """<h2>2 ТБ</h2>
<p>Apple выпускает iPhone 18 Pro и на 2 ТБ — версия рассчитана на профессиональную съёмку в ProRes и ProRes RAW.
Сейчас в ATOMM её нет в наличии.</p>""",
            },
            "summary": {
                256: "Снимаете в HEVC и храните галерею в облаке — хватит <b>256 ГБ</b> ({lo}).",
                512: "Часто пишете 4K-видео и качаете фильмы в дорогу — берите <b>512 ГБ</b> ({lo}).",
                1024: "Работаете с ProRes или Apple Log 2 и монтируете на телефоне — нужен <b>1 ТБ</b> ({lo}).",
                2048: "<b>2 ТБ</b> ({lo}) оправданы, только если iPhone заменяет вам рабочую камеру.",
            },
        },
        "body": """
<p>iPhone 18 Pro выпускается в четырёх версиях памяти — 256 ГБ, 512 ГБ, 1 ТБ и 2 ТБ. Слота для карты памяти нет,
поэтому объём выбирают один раз, при покупке. {mem_intro} Разбираемся, сколько места занимают система и видео
и какая версия подойдёт под ваш сценарий.</p>
{mem_table}

<h2>Сколько места останется</h2>
<p>По данным Apple, стандартная конфигурация iPhone 18 Pro занимает примерно от 12 до 24 ГБ: сюда входят iOS 27
и приложения Apple, часть из которых можно удалить (около 4,5 ГБ) и потом скачать снова из App Store. Ещё около 7 ГБ
занимают модели Apple Intelligence на устройстве — их можно удалить, если выключить Apple Intelligence. Остальное
место заполняет в первую очередь видео. Телефон снимает 4K Dolby Vision до 60 кадров/с на все камеры и до 120 кадров/с
на основную, поддерживает ProRes, ProRes RAW и Apple Log 2. Apple
предупреждает, что ролики ProRes бывают до 30 раз больше видео в HEVC, поэтому несколько съёмок в этом формате
заметно сокращают свободное место.</p>
<p>Самые тяжёлые режимы рассчитаны на внешний накопитель: ProRes в 4K при 120 кадрах/с iPhone 18 Pro записывает
на внешний диск через USB-C. Порт работает на скорости USB 3 — до 10 Гбит/с, если кабель тоже поддерживает 10 Гбит/с.</p>

{mem_sections}

<h2>Чем дополнить память</h2>
<p><b>«Фото iCloud».</b> Снимки и видео хранятся в облаке в исходном качестве, а с включённой оптимизацией хранилища
на телефоне остаются облегчённые копии. Объём облака при этом должен вмещать ваш архив.</p>
<p><b>Внешний SSD.</b> Подходит, чтобы писать ProRes напрямую и быстро освобождать место после съёмки.</p>

<h2>Итог: какой объём взять</h2>
{mem_summary}
<p>{mem_neighbors}Чип A20 Pro, камеры, экран 6,3 дюйма и батарея от объёма не зависят. Если ещё не решили,
нужен ли больший экран, загляните в сравнение <a href="/guides/iphone-18-pro-vs-18-pro-max/">«iPhone 18 Pro
или 18 Pro Max»</a>; про память старшей модели — в статье <a href="/guides/iphone-18-pro-max-skolko-pamyati/">«Сколько
памяти брать в iPhone 18 Pro Max»</a>.</p>
""",
    },
    # "crumb" — раздел в хлебных крошках (по умолчанию iPhone)
    "airpods-4-ili-airpods-5": {
        "title": "AirPods 4 или AirPods 5: чем отличаются и что выбрать",
        "seo_title": "AirPods 4 или AirPods 5: чем отличаются и что выбрать | ATOMM",
        "desc": "Сравнение AirPods 4 и AirPods 5 по официальным данным Apple: шумоподавление, время работы, кейс "
                "и беспроводная зарядка. Чем отличаются все четыре версии и какую выбрать.",
        "published": "2026-11-18",
        "modified": "2026-11-18",
        "models": ("airpods-4", "airpods-5"),
        "sources": SOURCES["airpods-4-vs-5"],
        "crumb": ("AirPods", "/catalog/airpods/"),
        "body": """
<p>AirPods 4 и AirPods 5 — открытые вкладыши Apple без амбушюр, и внешне они почти не отличаются. Сложность выбора
в другом: у каждого поколения по две версии, и они по-разному заряжаются, работают разное время и не все глушат шум.
Разбираем все четыре версии по официальным характеристикам Apple.</p>

<h2>Что у моделей одинаковое</h2>
<p>Обе модели работают на чипе H2 и подключаются по Bluetooth 5.3. Каждый наушник весит 4,3 г. Все кейсы заряжаются
через USB-C, а 5 минут в кейсе дают около часа прослушивания. На ножке у всех версий — датчик нажатия для управления. Полный набор функций доступен с устройствами
Apple, с остальными смартфонами AirPods работают как обычные Bluetooth-наушники с ограниченными возможностями.</p>

<h2>Чем отличаются</h2>
<table class="cmp">
<tr><th></th><th>AirPods 4</th><th>AirPods 4 с шумоподавлением</th><th>AirPods 5</th><th>AirPods 5 с кейсом беспроводной зарядки</th></tr>
<tr><td>Активное шумоподавление</td><td>нет</td><td>есть</td><td>есть</td><td>есть</td></tr>
<tr><td>Работа с шумоподавлением</td><td>—</td><td>до 4 ч</td><td>до 4 ч</td><td>до 5 ч</td></tr>
<tr><td>Работа без шумоподавления</td><td>до 5 ч</td><td>до 5 ч</td><td>до 6 ч</td><td>до 7 ч</td></tr>
<tr><td>С кейсом, с шумоподавлением</td><td>—</td><td>до 20 ч</td><td>до 20 ч</td><td>до 22 ч</td></tr>
<tr><td>С кейсом, без шумоподавления</td><td>до 30 ч</td><td>до 30 ч</td><td>—</td><td>—</td></tr>
<tr><td>Зарядка кейса</td><td>USB-C</td><td>USB-C, Qi, зарядка Apple Watch</td><td>USB-C</td><td>USB-C, Qi, зарядка Apple Watch</td></tr>
<tr><td>Динамик в кейсе для «Локатора»</td><td>нет</td><td>есть</td><td>нет</td><td>есть</td></tr>
<tr><td>Вес кейса</td><td>32,3 г</td><td>34,7 г</td><td>32,3 г</td><td>34,7 г</td></tr>
<tr><td>Цена в ATOMM</td><td colspan="2">{lo_1}</td><td colspan="2">{lo_2}</td></tr>
</table>
<p>Цены в таблице — минимальные по каждому поколению; стоимость конкретной версии видна в списке товаров ниже.</p>

<h2>Шумоподавление</h2>
<p>Главное, что изменилось в AirPods 5, — шумоподавление. Во-первых, теперь оно есть в обеих версиях, в том числе в самой
доступной: у AirPods 4 активное шумоподавление было только в старшей версии. Во-вторых, по данным Apple, AirPods 5 убирают
до 50% больше шума, чем AirPods 4 с шумоподавлением. Вместе с ним во всех версиях с шумоподавлением есть режим
«Прозрачность», адаптивный звук и автоматическое приглушение музыки, когда вы начинаете говорить.</p>
<p>Учтите, что это открытые вкладыши: они не закрывают слуховой канал так плотно, как модели с амбушюрами. Если нужна
максимальная изоляция от шума в метро или самолёте, посмотрите {link_airpods_pro_3}.</p>

<h2>Время работы и кейс</h2>
<p>Старшая версия AirPods 5 — в каталоге ATOMM она называется «беспроводная зарядка чехла» — работает дольше всех:
по данным Apple, до 5 часов с шумоподавлением, на час больше, чем AirPods 4 с шумоподавлением, и до 22 часов с кейсом.
Её кейс заряжается от Qi-совместимых зарядок и от зарядки Apple Watch, в нём есть динамик, чтобы найти кейс через
«Локатор» (для AirPods 5 нужна iOS 27 или новее), а громкость регулируется свайпом по ножке наушника.</p>
<p>У базовой версии AirPods 5 кейс проще — только USB-C, без динамика, но сами наушники с шумоподавлением работают столько же,
сколько AirPods 4 с шумоподавлением, — до 4 часов. Обычные AirPods 4 без шумоподавления играют до 5 часов, а с кейсом —
до 30 часов.</p>
<p>Защита от пыли, пота и воды у AirPods 4 — IP54: в них можно тренироваться, но не плавать. У AirPods 5 она выше —
IP57.</p>

<h2>Что выбрать</h2>
<p><b>AirPods 5 с кейсом беспроводной зарядки</b> — если нужны новое, более эффективное шумоподавление,
самое долгое время работы среди этих версий и кейс, который можно положить на беспроводную зарядку.</p>
<p><b>AirPods 5</b> — если шумоподавление нужно, а беспроводная зарядка кейса и динамик для поиска — нет.</p>
<p><b>AirPods 4 с шумоподавлением</b> — если устраивает шумоподавление прошлого поколения, а беспроводная зарядка кейса
важна.</p>
<p><b>AirPods 4</b> — если шумоподавление не нужно вовсе: музыка, подкасты и звонки в тихой обстановке. По времени работы
без шумоподавления они не уступают остальным версиям поколения.</p>
<p>Какая версия перед вами, указано в названии каждого товара. Другие наушники Apple, включая полноразмерные
и внутриканальные, собраны на странице <a href="/catalog/airpods/">AirPods</a>.</p>
""",
    },
}
