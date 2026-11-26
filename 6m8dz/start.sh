#!/bin/sh

echo "🔄 Применяем миграции..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "🧹 Собираем статику..."
python manage.py collectstatic --noinput

echo "🚀 Запускаем Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
