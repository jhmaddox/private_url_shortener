# *****************************************************************************
# app/permissions.py
# *****************************************************************************

import hmac

from django.conf import settings
from rest_framework.permissions import BasePermission


# *****************************************************************************
# SecretKeyIfConfiguredPermission
# *****************************************************************************

class SecretKeyIfConfiguredPermission(BasePermission):

    """
    a Permission that requires a secret key if one is configured

    """

    def has_permission(self, request, view):
        return bool(
            settings.PRIVATE_SHORTENER_API_SECRET_KEY is None or
            hmac.compare_digest(
                settings.PRIVATE_SHORTENER_API_SECRET_KEY,
                request.META.get('HTTP_AUTHORIZATION', ''),
            ),
        )
