# *****************************************************************************
# app/tests/test_shortened_url_model.py
# *****************************************************************************

from datetime import timedelta

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from ..models import ShortenedURL


# *****************************************************************************
# ShortenedURLModelTestCase
# *****************************************************************************

class ShortenedURLModelTestCase(TestCase):

    def test_is_expired(self):
        obj = ShortenedURL()
        self.assertEqual(obj.expires, None)
        self.assertEqual(obj.is_expired, False)
        obj.expires = timezone.now() + timedelta(seconds=1)
        self.assertEqual(obj.is_expired, False)
        obj.expires = timezone.now() - timedelta(seconds=1)
        self.assertEqual(obj.is_expired, True)

    @override_settings(SECRET_KEY='12345')
    def test_get_absolute_url(self):
        obj = ShortenedURL()
        obj.pk = 42
        self.assertEqual(obj.get_absolute_url(), '/g/70jS4E/')
        obj.pk = 88888888
        self.assertEqual(obj.get_absolute_url(), '/60y3k/567iT7/')

    def test_pk_encoded(self):
        obj = ShortenedURL()
        obj.pk = 1
        self.assertEqual(obj.pk_encoded, '1')
        obj.pk = 42
        self.assertEqual(obj.pk_encoded, 'g')
        obj.pk = 10423864
        self.assertEqual(obj.pk_encoded, 'hjiq')

    @override_settings(SECRET_KEY='12345')
    def test_sig(self):
        obj = ShortenedURL()
        obj.pk = 1
        self.assertEqual(obj.sig, '79ksGr')
        obj.pk = 42
        self.assertEqual(obj.sig, '70jS4E')
        obj.pk = 1e9
        self.assertEqual(obj.sig, '4HebeE')

    @override_settings(SECRET_KEY='12345', PRIVATE_SHORTENER_SIG_LENGTH=16)
    def test_sig_length_setting(self):
        obj = ShortenedURL()
        obj.pk = 1
        self.assertEqual(obj.sig, '79ksGrFrR1rvpubgZwL4vX'[:16])
        obj.pk = 42
        self.assertEqual(obj.sig, '70jS4EMCln1Ut3gRe7q64z'[:16])
        obj.pk = 1e9
        self.assertEqual(obj.sig, '4HebeEnldSdqRM1RP4dTYS'[:16])
