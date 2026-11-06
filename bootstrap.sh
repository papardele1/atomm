#!/usr/bin/env bash
# Установка/обновление ATOMM одной командой:
#   curl -fsSL https://raw.githubusercontent.com/papardele1/atomm/main/bootstrap.sh | bash
set -euo pipefail
[ "$(id -u)" = 0 ] || { echo "Нужен root"; exit 1; }
export DEBIAN_FRONTEND=noninteractive
command -v git >/dev/null || { apt-get update -q && apt-get install -y -q git >/dev/null; }
if [ -d /root/atomm-src/.git ]; then
  git -C /root/atomm-src fetch -q origin main && git -C /root/atomm-src reset -q --hard origin/main
else
  git clone -q https://github.com/papardele1/atomm /root/atomm-src
fi
# ввод (токен Telegram, e-mail) берём с терминала, а не из curl
bash /root/atomm-src/install.sh < /dev/tty
