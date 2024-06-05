#!/bin/sh

# Запуск Python-скрипта для добавления клиентов
python3 /etc/v2ray/add_clients.py

# Запуск v2ray
exec v2ray run -c /etc/v2ray/config.json
