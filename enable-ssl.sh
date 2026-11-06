#!/usr/bin/env bash
# Подключение бесплатного HTTPS (Let's Encrypt) для atomm.store.
# Работает, только когда в DNS домена A-запись указывает на этот сервер.
set -euo pipefail
DOMAIN="atomm.store"
SERVER_IP="82.114.226.70"

NAMES=()
for n in "$DOMAIN" "www.$DOMAIN"; do
  ip=$(getent ahostsv4 "$n" | awk 'NR==1{print $1}' || true)
  if [ "$ip" = "$SERVER_IP" ]; then NAMES+=("-d" "$n"); else echo "• $n → ${ip:-нет записи} (нужно $SERVER_IP) — пропускаю"; fi
done
if [ ${#NAMES[@]} -eq 0 ]; then
  echo "DNS ещё не указывает на сервер. Добавьте A-записи у регистратора и повторите через 15–60 минут."
  exit 1
fi
read -rp "E-mail для уведомлений Let's Encrypt (можно оставить пустым): " EMAIL || EMAIL=""
if [ -n "$EMAIL" ]; then MAIL=(-m "$EMAIL"); else MAIL=(--register-unsafely-without-email); fi
certbot --nginx "${NAMES[@]}" "${MAIL[@]}" --agree-tos --redirect --non-interactive
echo "HTTPS подключён. Сертификат будет продлеваться автоматически."
