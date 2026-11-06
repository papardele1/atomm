# ATOMM — интернет-магазин техники

Установка или обновление на сервере (Ubuntu 22.04/24.04), от root:

```
curl -fsSL https://raw.githubusercontent.com/papardele1/atomm/main/bootstrap.sh | bash
```

Подробности — в `README.txt`.

## Сервер с mskm2bot (Docker)

На сервере 82.114.226.70 порты 80/443 занимает Caddy из mskm2bot, поэтому ATOMM работает в Docker:
`docker-compose.yml` (сервисы `api` — сайт + заказы, `parser` — цены каждые 4 часа), а Caddy из
mskm2bot проксирует `atomm.store` на `atomm-api:8080` через сеть `edge`.
Деплой: в репозитории mskm2bot → Actions → «ATOMM деплой» → Run workflow.
Секреты там же (необязательно): `ATOMM_TG_TOKEN`, `ATOMM_TG_CHAT`, `ATOMM_PROXY`.
