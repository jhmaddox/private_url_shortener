# *****************************************************************************
# app/models.py
# *****************************************************************************

import hmac

from baseconvert import base
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


# *****************************************************************************
# ShortenedURL
# *****************************************************************************

class ShortenedURL(models.Model):

    """
    a Model that represents a shortened url

    """

    url = models.URLField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return 'pk={}, url={}'.format(self.pk, self.get_absolute_url())

    def get_absolute_url(self):
        return reverse(
            'app:redirect-short',
            kwargs={
                'pk_encoded': self.pk_encoded,
                'sig': self.sig,
            },
        )

    @property
    def is_expired(self):
        return bool(self.expires and self.expires < timezone.now())

    @property
    def pk_encoded(self):
        return base(self.pk, 10, 62, string=True)

    @property
    def sig(self):
        key_encoded = settings.SECRET_KEY.encode('utf-8')
        pk_encoded = self.pk_encoded.encode('utf-8')
        sig_16 = hmac.new(key=key_encoded, msg=pk_encoded).hexdigest()
        sig_10 = int(sig_16, base=16)
        sig_62 = base(sig_10, 10, 62, string=True)
        return sig_62[:settings.PRIVATE_SHORTENER_SIG_LENGTH]
