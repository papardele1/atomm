#!/usr/bin/env bash
# Установка сайта ATOMM на VPS (Ubuntu 22.04/24.04). Запуск: sudo bash install.sh
# Повторный запуск безопасен: обновляет код сайта и сервера, настройки Telegram не трогает.
set -euo pipefail

DOMAIN="atomm.store"
SERVER_IP="82.114.226.70"
SRC="$(cd "$(dirname "$0")" && pwd)"

say(){ printf '\n\033[1m▶ %s\033[0m\n' "$*"; }
[ "$(id -u)" = 0 ] || { echo "Запустите от root: sudo bash install.sh"; exit 1; }

say "1/7 Устанавливаю пакеты (nginx, python, certbot)…"
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q nginx python3-venv python3-pip certbot python3-certbot-nginx ufw curl sqlite3 >/dev/null

say "2/7 Копирую сайт и сервер…"
id atomm >/dev/null 2>&1 || useradd --system --home /opt/atomm --shell /usr/sbin/nologin atomm
mkdir -p /opt/atomm /var/www/atomm /var/lib/atomm /etc/atomm
rm -rf /opt/atomm/app && cp -r "$SRC/app" /opt/atomm/app
cp "$SRC/requirements.txt" /opt/atomm/
cp "$SRC/site/index.html" "$SRC/site/catalog.html" "$SRC/site/privacy.html" /var/www/atomm/
# каталог берём из пакета только при первой установке — дальше его обновляет парсер
[ -f /var/www/atomm/catalog.json ] || cp "$SRC/site/catalog.json" /var/www/atomm/
chown -R atomm:atomm /var/www/atomm /var/lib/atomm /opt/atomm

say "3/7 Готовлю окружение Python…"
[ -x /opt/atomm/venv/bin/python ] || python3 -m venv /opt/atomm/venv
/opt/atomm/venv/bin/pip install -q --upgrade pip
/opt/atomm/venv/bin/pip install -q -r /opt/atomm/requirements.txt

say "4/7 Подключаю Telegram для уведомлений о заказах…"
if [ ! -f /etc/atomm/env ]; then
  TG_TOKEN=""; TG_CHAT=""
  while :; do
    read -rsp "Вставьте токен Telegram-бота от @BotFather (ввод скрыт) и нажмите Enter: " TG_TOKEN; echo
    if curl -fs "https://api.telegram.org/bot${TG_TOKEN}/getMe" >/dev/null; then echo "Токен принят."; break; fi
    echo "Токен не подошёл, попробуйте ещё раз."
  done
  echo "Теперь откройте своего бота в Telegram и отправьте ему /start. Жду до 3 минут…"
  for _ in $(seq 1 36); do
    TG_CHAT=$(curl -fs "https://api.telegram.org/bot${TG_TOKEN}/getUpdates" | python3 -c 'import sys,json
d=json.load(sys.stdin); r=[u["message"]["chat"]["id"] for u in d.get("result",[]) if "message" in u]
print(r[-1] if r else "")' || true)
    [ -n "$TG_CHAT" ] && break
    sleep 5
  done
  [ -n "$TG_CHAT" ] || { echo "Не дождался /start. Запустите install.sh ещё раз."; exit 1; }
  umask 077
  cat > /etc/atomm/env <<EOF
TG_TOKEN=${TG_TOKEN}
TG_CHAT=${TG_CHAT}
ATOMM_CATALOG=/var/www/atomm/catalog.json
ATOMM_DB=/var/lib/atomm/orders.db
# ATOMM_PROXY=http://user:pass@host:port   # раскомментируйте, если Store77 начнёт блокировать сервер
EOF
  chown root:atomm /etc/atomm/env; chmod 640 /etc/atomm/env; umask 022
  curl -fs -X POST "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" -d chat_id="$TG_CHAT" \
       --data-urlencode text="✅ ATOMM подключён. Сюда будут приходить новые заказы." >/dev/null || true
  echo "Готово: проверочное сообщение отправлено в Telegram."
else
  echo "Настройки Telegram уже есть (/etc/atomm/env) — пропускаю."
fi

say "5/7 Настраиваю службы (сервер заказов и парсер по расписанию)…"
cat > /etc/systemd/system/atomm-api.service <<'EOF'
[Unit]
Description=ATOMM order API
After=network-online.target

[Service]
User=atomm
EnvironmentFile=/etc/atomm/env
WorkingDirectory=/opt/atomm/app
ExecStart=/opt/atomm/venv/bin/uvicorn api:app --host 127.0.0.1 --port 8080 --proxy-headers
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
cat > /etc/systemd/system/atomm-parser.service <<'EOF'
[Unit]
Description=ATOMM Store77 price parser
After=network-online.target

[Service]
Type=oneshot
User=atomm
EnvironmentFile=/etc/atomm/env
WorkingDirectory=/opt/atomm/app
ExecStart=/opt/atomm/venv/bin/python /opt/atomm/app/parser.py
TimeoutStartSec=3h
Nice=10
EOF
cat > /etc/systemd/system/atomm-parser.timer <<'EOF'
[Unit]
Description=Run ATOMM parser every 4 hours

[Timer]
OnCalendar=*-*-* 00/4:15:00
RandomizedDelaySec=20min
Persistent=true

[Install]
WantedBy=timers.target
EOF
systemctl daemon-reload
systemctl enable --now atomm-api.service >/dev/null
systemctl restart atomm-api.service
systemctl enable --now atomm-parser.timer >/dev/null

say "6/7 Настраиваю веб-сервер nginx…"
LISTEN6=""; [ -s /proc/net/if_inet6 ] && LISTEN6="listen [::]:80 default_server;"
cat > /etc/nginx/sites-available/atomm <<EOF
server {
    listen 80 default_server;
    ${LISTEN6}
    server_name ${DOMAIN} www.${DOMAIN} ${SERVER_IP} _;
    root /var/www/atomm;
    index index.html;
    server_tokens off;
    gzip on;
    gzip_types application/json text/css application/javascript image/svg+xml;
    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy strict-origin-when-cross-origin always;

    location = /catalog.json { add_header Cache-Control "no-cache"; add_header X-Content-Type-Options nosniff always; }
    location /api/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        client_max_body_size 64k;
    }
    location / { try_files \$uri \$uri/ =404; }
}
EOF
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/atomm /etc/nginx/sites-enabled/atomm
nginx -t
systemctl reload nginx

# файрвол: открываем порт(ы) SSH, на которых реально работает сервер, затем 80/443
SSH_PORTS=$( (sshd -T 2>/dev/null || true) | awk '/^port /{print $2}')
[ -n "$SSH_PORTS" ] || SSH_PORTS=22
for p in $SSH_PORTS; do ufw allow "$p"/tcp >/dev/null; done
ufw allow 'Nginx Full' >/dev/null
ufw --force enable >/dev/null

say "7/7 Подключаю HTTPS…"
cp "$SRC/enable-ssl.sh" /opt/atomm/enable-ssl.sh && chmod +x /opt/atomm/enable-ssl.sh
bash /opt/atomm/enable-ssl.sh || echo "HTTPS пока не подключён — запустите позже: sudo bash /opt/atomm/enable-ssl.sh"

say "Первый запуск парсера цен (идёт в фоне 15–30 минут)…"
systemctl start --no-block atomm-parser.service

cat <<EOF

────────────────────────────────────────────
 ATOMM установлен.
   Сайт:          http://${SERVER_IP}  (и https://${DOMAIN}, когда заработает SSL)
   Проверка API:  curl -s http://127.0.0.1:8080/api/health
   Лог парсера:   journalctl -u atomm-parser -f
   Заказы:        sqlite3 /var/lib/atomm/orders.db 'select * from orders order by id desc limit 10'
────────────────────────────────────────────
EOF
