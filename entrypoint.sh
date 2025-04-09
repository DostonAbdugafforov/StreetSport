#!/bin/bash

# Xatolarni qayd qilish
set -e

# Loyihaning asosiy papkasiga o'tish
cd /app

# Migrations fayllarini yaratish
echo "Migrations yaratilmoqda..."
python3 manage.py makemigrations

# Migrationsni bajarish
echo "Migrations bajarilmoqda..."
python3 manage.py migrate

# Serverni ishga tushirish
echo "Server ishga tushirilmoqda..."
python3 manage.py runserver 0.0.0.0:8000

