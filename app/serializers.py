# *****************************************************************************
# app/serializers.py
# *****************************************************************************

from rest_framework import serializers

from .models import ShortenedURL


# *****************************************************************************
# ShortenedURLSerializer
# *****************************************************************************

class ShortenedURLSerializer(serializers.ModelSerializer):

    """
    a Serializer for app.ShortenedURL objects

    """

    result_url = serializers.URLField(
        source='get_absolute_url',
        read_only=True,
    )

    class Meta:
        model = ShortenedURL
        fields = (
            'created',
            'expires',
            'result_url',
            'url',
        )
