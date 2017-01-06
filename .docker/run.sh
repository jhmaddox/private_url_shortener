#!/bin/sh

sleep 8 # give database time to boot
python manage.py migrate
gunicorn -b 0.0.0.0:8000 private_url_shortener.wsgi:application
