#!/usr/bin/env bash
# سكربت بناء المشروع على Render

echo "📦 تثبيت المتطلبات..."
pip install -r requirements.txt

echo "🛠️ تنفيذ collectstatic..."
python manage.py collectstatic --noinput
