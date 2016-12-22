# *****************************************************************************
# app/urls.py
# *****************************************************************************

from django.conf.urls import url
from rest_framework import routers


from .views import RedirectShortenedURLView, ShortenedURLAPIView


# *****************************************************************************
# urlpatterns
# *****************************************************************************

router = routers.SimpleRouter()

router.register(
    base_name='shortened_url',
    prefix=r'api/shortened-url',
    viewset=ShortenedURLAPIView,
)

urlpatterns = router.urls + [
    url(
        r'^(?P<pk_encoded>\w+)/(?P<sig>\w+)/$',
        RedirectShortenedURLView.as_view(),
        name='redirect-short',
    ),
]
