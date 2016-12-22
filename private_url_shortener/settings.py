# *****************************************************************************
# private_url_shortener/settings.py
# *****************************************************************************

import os


# *****************************************************************************
# Django conf
# *****************************************************************************

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', '')]
AUTH_PASSWORD_VALIDATORS = []
CSRF_COOKIE_SECURE = os.environ.get('SSL_ONLY') == 'True'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': os.environ.get(
            'DATABASE_ENGINE',
            'django.db.backends.sqlite3',
        ),
        'NAME': os.environ.get(
            'DATABASE_NAME',
            os.path.join(BASE_DIR, 'db.sqlite3'),
        ),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    },
}

DEBUG = os.environ.get('DEBUG') == 'False' or True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'app',
]

LANGUAGE_CODE = 'en-us'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

ROOT_URLCONF = 'private_url_shortener.urls'

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'I am a big dummy who never changed the secret key',
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

PRIVATE_SHORTENER_API_SECRET_KEY = os.environ.get('PRIVATE_SHORTENER_API_SECRET_KEY')
PRIVATE_SHORTENER_SIG_LENGTH = os.environ.get('PRIVATE_SHORTENER_SIG_LENGTH', 6)
PRIVATE_SHORTENER_REDIRECT_EXPIRED_URL = os.environ.get('PRIVATE_SHORTENER_REDIRECT_EXPIRED_URL')
PRIVATE_SHORTENER_REDIRECT_INVALID_URL = os.environ.get('PRIVATE_SHORTENER_REDIRECT_INVALID_URL')

SESSION_COOKIE_SECURE = os.environ.get('SSL_ONLY') == 'True'
STATIC_ROOT = os.environ.get('STATIC_ROOT')
STATIC_URL = os.environ.get('STATIC_URL', '/static/')

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')
WSGI_APPLICATION = 'private_url_shortener.wsgi.application'
USE_I18N = True
USE_L10N = True
USE_TZ = True
