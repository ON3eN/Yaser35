#!/usr/bin/env bash
echo "📦 تثبيت المتطلبات..."
pip install -r requirements.txt

echo "🛠️ جمع الملفات الثابتة..."
python manage.py collectstatic --noinput
