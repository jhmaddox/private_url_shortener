# *****************************************************************************
# app/views.py
# *****************************************************************************

import hmac
import logging

from baseconvert import base
from django.conf import settings
from django.http import Http404
from django.views.generic.base import RedirectView
from rest_framework import mixins, viewsets

from .models import ShortenedURL
from .permissions import SecretKeyIfConfiguredPermission
from .serializers import ShortenedURLSerializer


# *****************************************************************************
# RedirectShortenedURLView
# *****************************************************************************

class RedirectShortenedURLView(RedirectView):

    """
    a RedirectView that redirects to the shortened url

    """

    logger = logging.getLogger(__name__)

    def get_redirect_url(self, pk_encoded, sig):

        pk = base(pk_encoded, 62, 10, string=True)
        short_url = None
        result = None

        try:
            short_url = ShortenedURL.objects.get(pk=pk)
        except ShortenedURL.DoesNotExist:
            pass

        valid_request = short_url and hmac.compare_digest(short_url.sig, sig)

        if valid_request and not short_url.is_expired:
            result = short_url.url
        elif valid_request and short_url.is_expired:
            result = settings.PRIVATE_SHORTENER_REDIRECT_EXPIRED_URL
            self.log_expired_url(short_url)
        elif not valid_request and short_url:
            result = settings.PRIVATE_SHORTENER_REDIRECT_INVALID_URL
            self.log_invalid_sig(short_url, sig)
        else:
            result = settings.PRIVATE_SHORTENER_REDIRECT_INVALID_URL
            self.log_invalid_pk(pk_encoded)

        self.log_result(result)

        if not result:
            raise Http404

        return result

    def log_expired_url(self, short_url):
        self.logger.info(
            'Redirect blocked, {short_url} expired on {expires}'.format(
                expires=short_url.expires,
                short_url=repr(short_url),
            ),
        )

    def log_invalid_pk(self, pk_encoded):
        self.logger.info(
            'Redirect blocked, invalid pk_encoded "{pk_encoded}"'.format(
                pk_encoded=pk_encoded,
            ),
        )

    def log_invalid_sig(self, short_url, sig):
        self.logger.info(
            'Redirect blocked, invalid sig "{sig}" for {short_url}'.format(
                short_url=repr(short_url),
                sig=sig,
            ),
        )

    def log_result(self, result):
        self.logger.debug(
            'Redirecting "{short_url}" to "{result}"'.format(
                result=result or '404',
                short_url=self.request.path,
            ),
        )


# *****************************************************************************
# ShortenedURLAPIView
# *****************************************************************************

class ShortenedURLAPIView(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):

    """
    an APIView for app.ShortenedURL objects

    """

    logger = logging.getLogger(__name__)
    permission_classes = [SecretKeyIfConfiguredPermission]
    serializer_class = ShortenedURLSerializer

    def log_permission_denied(self):
        api_key = self.request.META.get('HTTP_AUTHORIZATION')
        self.logger.warn(
            'Access Denied: {}. Failed to save URL.'.format(
                'Invalid API key "{}"'.format(api_key)
                if api_key else
                'Missing API key'
            ),
        )

    def log_success(self, short_url):
        self.logger.info(
            'Saved URL "{url}" as "{result_url}"'.format(
                url=short_url.url,
                result_url=short_url.get_absolute_url(),
            ),
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        self.log_success(instance)

    def permission_denied(self, *args, **kwargs):
        self.log_permission_denied()
        return super().permission_denied(*args, **kwargs)
