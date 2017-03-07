# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from .util import TranslatedField

class ArticleIndexPage(Page):
    title_fr = models.CharField(max_length=255, default="")
    trans_title = TranslatedField(
        'title',
        'title_fr',
    )
    content_panels = Page.content_panels + [
        FieldPanel('title_fr'),
    ]
    def get_context(self, request):
        context = super(ArticleIndexPage, self).get_context(request)
        # Add extra variables and return the updated context
        context['article_entries'] = ArticlePage.objects.child_of(self).live()
        return context
    class Meta:
        verbose_name = "Rubrik"

class ArticlePage(Page):
    title_fr = models.CharField(max_length=255, default="")
    trans_title = TranslatedField(
        'title',
        'title_fr',
    )

    intro_de = RichTextField(default='')
    intro_fr = RichTextField(default='')
    trans_intro = TranslatedField(
        'intro_de',
        'intro_fr',
    )

    body_de = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('section', blocks.CharBlock(classname="full title")),
    ], null=True, blank=True)
    body_fr = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('section', blocks.CharBlock(classname="full title")),
    ], null=True, blank=True)
    trans_body = TranslatedField(
        'body_de',
        'body_fr',
    )

    date = models.DateField("Date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body_de'),
        index.SearchField('body_fr'),
        index.SearchField('title'),
        index.SearchField('title_fr'),
        index.SearchField('intro_de'),
        index.SearchField('intro_fr'),
    ]
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('intro_de'),
            StreamFieldPanel('body_de'),
        ], heading="Deutsch"),
        MultiFieldPanel([
            FieldPanel('title_fr'),
            FieldPanel('intro_fr'),
            StreamFieldPanel('body_fr'),
        ], heading="Français"),
    ]
    promote_panels = [
        FieldPanel('date'),
        ImageChooserPanel('feed_image'),
        InlinePanel('related_links', label="Links"),
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]
    parent_page_types = ['home.ArticleIndexPage']
    subpage_types = []
    class Meta:
        verbose_name = "Artikel"

class ArticleRelatedLink(Orderable):
    page = ParentalKey(ArticlePage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()
    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

class InfoBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    photo = ImageChooserBlock()
    summary = blocks.RichTextBlock(required=True)
    action = blocks.CharBlock()
    url = blocks.URLBlock()

class HomePage(Page):
    intro_de = RichTextField(default='')
    intro_fr = RichTextField(default='')
    trans_intro = TranslatedField(
        'intro_de',
        'intro_fr',
    )

    body_de = RichTextField(default='')
    body_fr = RichTextField(default='')
    trans_body = TranslatedField(
        'body_de',
        'body_fr',
    )

    infos_de = StreamField([
        ('info', InfoBlock())
    ], null=True, blank=True)
    infos_fr = StreamField([
        ('info', InfoBlock())
    ], null=True, blank=True)
    trans_infos = TranslatedField(
        'infos_de',
        'infos_fr',
    )

    def get_articles(self):
        return ArticleIndexPage.objects.descendant_of(self).live().order_by('-date').select_related('owner')

    content_panels = Page.content_panels + [
        FieldPanel('intro_de', classname="full"),
        FieldPanel('intro_fr', classname="full"),
        FieldPanel('body_de', classname="full"),
        FieldPanel('body_fr', classname="full"),
        StreamFieldPanel('infos_de'),
        StreamFieldPanel('infos_fr'),
    ]
