# *****************************************************************************
# private_url_shortener/wsgi.py
# *****************************************************************************

import os

from django.core.wsgi import get_wsgi_application


# *****************************************************************************
# application
# *****************************************************************************

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'private_url_shortener.settings',
)

application = get_wsgi_application()
