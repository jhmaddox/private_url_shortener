# *****************************************************************************
# app/tests/test_redirect_short.py
# *****************************************************************************

from datetime import timedelta

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from ..models import ShortenedURL


# *****************************************************************************
# RedirectShortenedURLTestCase
# *****************************************************************************

class RedirectShortenedURLTestCase(TestCase):

    def setUp(self):
        self.short_url = ShortenedURL.objects.create(
            url='https://adecco.trymya.io',
        )

    @override_settings(PRIVATE_SHORTENER_REDIRECT_EXPIRED_URL=None)
    def test_expires(self):
        self.short_url.expires = timezone.now() - timedelta(seconds=1)
        self.short_url.save()
        response = self.client.get(self.short_url.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    @override_settings(
        PRIVATE_SHORTENER_REDIRECT_EXPIRED_URL='http://expired.com',
    )
    def test_expires_redirect_setting(self):
        self.short_url.expires = timezone.now() - timedelta(seconds=1)
        self.short_url.save()
        response = self.client.get(self.short_url.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://expired.com')

    @override_settings(PRIVATE_SHORTENER_REDIRECT_INVALID_URL=None)
    def test_invalid_pk(self):
        response = self.client.get('/zzzzzzzz/abcdef/')
        self.assertEqual(response.status_code, 404)

    @override_settings(
        PRIVATE_SHORTENER_REDIRECT_INVALID_URL='http://invalid.com',
    )
    def test_invalid_pk_redirect_setting(self):
        response = self.client.get('/zzzzzzzz/abcdef/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://invalid.com')

    @override_settings(PRIVATE_SHORTENER_REDIRECT_INVALID_URL=None)
    def test_invalid_sig(self):
        url = '/{}/invalidsig/'.format(self.short_url.pk_encoded)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @override_settings(
        PRIVATE_SHORTENER_REDIRECT_INVALID_URL='http://invalid.com',
    )
    def test_invalid_sig_redirect_setting(self):
        url = '/{}/invalidsig/'.format(self.short_url.pk_encoded)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://invalid.com')

    def test_redirect(self):
        response = self.client.get(self.short_url.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://adecco.trymya.io')
        short_url2 = ShortenedURL.objects.create(url='http://google.com')
        response = self.client.get(short_url2.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://google.com')
