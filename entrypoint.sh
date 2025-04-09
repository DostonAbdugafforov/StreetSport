#!/bin/bash

# Xatolarni qayd qilish
set -e

# Loyihaning asosiy papkasiga o'tish
cd /app

# Migrations fayllarini yaratish
echo "Migrations yaratilmoqda..."
python manage.py makemigrations

# Migrationsni bajarish
echo "Migrations bajarilmoqda..."
python manage.py migrate

# Gunicorn yordamida serverni ishga tushirish
echo "Server ishga tushirilmoqda..."
pip install gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000

