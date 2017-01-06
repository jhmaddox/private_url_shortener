#!/bin/sh

sleep 14 # give database time to boot
python manage.py collectstatic --no-input
python manage.py migrate
gunicorn -b 0.0.0.0:8000 private_url_shortener.wsgi:application
