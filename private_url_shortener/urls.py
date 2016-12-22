# *****************************************************************************
# private_url_shortener/urls.py
# *****************************************************************************

from django.conf.urls import include, url
from django.contrib import admin


# *****************************************************************************
# urlpatterns
# *****************************************************************************

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('app.urls', namespace='app')),
]
