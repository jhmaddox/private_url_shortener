# *****************************************************************************
# app/admin.py
# *****************************************************************************

from django.contrib import admin

from . import models


# *****************************************************************************
# ShortenedURLAdmin
# *****************************************************************************

@admin.register(models.ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):

    """
    a ModelAdmin for app.ShortenedURL

    """

    fields = (
        'created',
        'expires',
        'url',
        'get_absolute_url',
    )

    list_display = (
        'pk',
        'created',
        'expires',
        'url',
    )

    list_display_links = (
        'pk',
        'created',
        'expires',
        'url',
    )

    readonly_fields = (
        'created',
        'get_absolute_url',
    )

    search_fields = (
        'url',
    )
