# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailsnippets.models import register_snippet

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from .util import TranslatedField

@register_snippet
class Contact(models.Model):
    title = models.CharField(max_length=255, default="")
    title_fr = models.CharField(max_length=255, default="")
    trans_title = TranslatedField(
        'title',
        'title_fr',
    )
    address = models.TextField(default="", blank=True)
    phone = models.CharField(max_length=40, default="")
    email = models.CharField(max_length=40, default="")
    www = models.URLField(null=True, blank=True)

    panels = Page.content_panels + [
        FieldPanel('title_fr'),
        FieldPanel('address'),
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('www'),
    ]

    def __str__(self):
        return self.trans_title
