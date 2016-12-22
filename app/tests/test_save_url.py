# *****************************************************************************
# app/tests/test_save_url.py
# *****************************************************************************

from datetime import timedelta

from django.test.utils import override_settings
from django.utils import timezone
from rest_framework.test import APITestCase

from ..models import ShortenedURL


# *****************************************************************************
# SaveURLTestCase
# *****************************************************************************

class SaveURLTestCase(APITestCase):

    @override_settings(PRIVATE_SHORTENER_API_SECRET_KEY=None)
    def test_expires(self):

        self.assertEqual(ShortenedURL.objects.count(), 0)

        expires = timezone.now() + timedelta(seconds=1)

        response = self.client.post('/api/shortened-url/', {
            'url': 'http://some.private.link/secret',
            'expires': expires.isoformat(),
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data['url'],
            'http://some.private.link/secret',
        )
        self.assertEqual(ShortenedURL.objects.count(), 1)
        obj = ShortenedURL.objects.first()
        self.assertEqual(obj.url, 'http://some.private.link/secret')
        self.assertEqual(obj.expires, expires)
        self.assertEqual(response.data['result_url'], obj.get_absolute_url())

    @override_settings(PRIVATE_SHORTENER_API_SECRET_KEY=None)
    def test_invalid_url(self):

        response = self.client.post('/api/shortened-url/', {
            'url': 'this is not a URL',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {
            'url': ['Enter a valid URL.'],
        })

    @override_settings(PRIVATE_SHORTENER_API_SECRET_KEY='12345')
    def test_invalid_api_secret_key(self):
        response = self.client.post('/api/shortened-url/', {
            'url': 'http://google.com',
        })
        self.assertEqual(response.status_code, 403)
        self.client.credentials(HTTP_AUTHORIZATION='abcdef')
        response = self.client.post('/api/shortened-url/', {
            'url': 'http://google.com',
        })
        self.assertEqual(response.status_code, 403)

    @override_settings(PRIVATE_SHORTENER_API_SECRET_KEY=None)
    def test_save_url(self):

        self.assertEqual(ShortenedURL.objects.count(), 0)

        response = self.client.post('/api/shortened-url/', {
            'url': 'http://google.com',
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['url'], 'http://google.com')
        self.assertEqual(ShortenedURL.objects.count(), 1)
        obj = ShortenedURL.objects.first()
        self.assertEqual(obj.url, 'http://google.com')
        self.assertEqual(obj.expires, None)
        self.assertEqual(response.data['result_url'], obj.get_absolute_url())

    @override_settings(PRIVATE_SHORTENER_API_SECRET_KEY='12345')
    def test_save_url_with_api_key(self):

        self.assertEqual(ShortenedURL.objects.count(), 0)
        self.client.credentials(HTTP_AUTHORIZATION='12345')

        response = self.client.post('/api/shortened-url/', {
            'url': 'http://google.com',
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['url'], 'http://google.com')
        self.assertEqual(ShortenedURL.objects.count(), 1)
        obj = ShortenedURL.objects.first()
        self.assertEqual(obj.url, 'http://google.com')
        self.assertEqual(obj.expires, None)
        self.assertEqual(response.data['result_url'], obj.get_absolute_url())
