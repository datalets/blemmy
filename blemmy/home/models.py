# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.api import APIField
from wagtail.wagtailcore.blocks import StructBlock, CharBlock, URLBlock, RichTextBlock
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

class ArticleIndexPage(Page):
    intro = RichTextField(default='', blank=True)

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
                FieldPanel('intro'),
                ImageChooserPanel('feed_image'),
            ],
            heading="Un MultiFieldPanel",
            classname="collapsible collapsed",
    ),
    ]

    def get_context(self, request):
        context = super(ArticleIndexPage, self).get_context(request)
        articles = ArticlePage.objects.child_of(self).live()
        context['articles'] = articles
        subcategories = ArticleIndexPage.objects.child_of(self).live()
        context['subcategories'] = subcategories
        return context

    subpage_types = [
        'home.ArticlePage',
        'home.ArticleIndexPage',
    ]
    class Meta:
        verbose_name = "Index page"

class ArticlePage(Page):
    intro = RichTextField(default='', blank=True)

    body = StreamField([
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('section', CharBlock(classname="full title")),
    ], null=True, blank=True)

    is_featured = models.BooleanField(default=False, verbose_name="Featured",
        help_text="Is this a featured entry?")

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    postdate = models.DateField(default='YYYY-MM-DD', blank=True)

    api_fields = [
        APIField('intro'),
        APIField('body'),
        APIField('feed_image'),
        APIField('is_featured'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('title',    partial_match=True, boost=10),
        index.SearchField('intro',    partial_match=True),
        index.SearchField('body',     partial_match=True),
    ]
    content_panels = Page.content_panels + [
        ImageChooserPanel('feed_image'),
        FieldPanel('intro', classname="col7"),
        FieldPanel('postdate', classname="col5"),
        MultiFieldPanel([
            StreamFieldPanel('body'),
            ],
            heading="Content",
            classname="collapsible collapsed col12",
    ),
    ]
    promote_panels = [
        InlinePanel('related_links', label="Links"),
        MultiFieldPanel([
            FieldPanel('is_featured'),
        ], heading="Publication"),
        MultiFieldPanel(Page.promote_panels, "Settings"),
    ]

    subpage_types = ['wagtailcore.Page']
    class Meta:
        verbose_name = "Web page"

class ArticleRelatedLink(Orderable):
    page = ParentalKey(ArticlePage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()
    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]
