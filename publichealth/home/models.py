from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index

from .util import TranslatedField

class HomePage(Page):
    title_fr = models.CharField(max_length=255, default="")

    body_de = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], null=True, blank=True)
    body_fr = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], null=True, blank=True)

    translated_title = TranslatedField(
        'title',
        'title_fr',
    )
    body = TranslatedField(
        'body_de',
        'body_fr',
    )

    search_fields = Page.search_fields + [
        index.SearchField('body_de'),
        index.SearchField('body_fr'),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('title_fr'),
        StreamFieldPanel('body_de'),
        StreamFieldPanel('body_fr'),
    ]
