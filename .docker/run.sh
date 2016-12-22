#!/bin/sh
python manage.py migrate
gunicorn -b 0.0.0.0:8000 secure_shortener.wsgi:application
