#!/usr/bin/env bash

echo "📦 تثبيت المتطلبات..."
pip install -r requirements.txt

echo "🗃️ ترحيل قاعدة البيانات..."
python manage.py migrate --noinput

echo "🛠️ جمع الملفات الثابتة (static)..."
python manage.py collectstatic --noinput

echo "✅ الانتهاء من السكربت ✅"
