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
    translated_title = TranslatedField(
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

class ArticlePage(Page):
    title_fr = models.CharField(max_length=255, default="")
    translated_title = TranslatedField(
        'title',
        'title_fr',
    )

    date = models.DateField("Date")

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
    body = TranslatedField(
        'body_de',
        'body_fr',
    )

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
        index.FilterField('date'),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('title_fr'),
        FieldPanel('date'),
        StreamFieldPanel('body_de'),
        StreamFieldPanel('body_fr'),
        InlinePanel('related_links', label="Related links"),
    ]
    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]
    parent_page_types = ['home.ArticleIndexPage']
    subpage_types = []

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
    summary = blocks.RichTextBlock()
    action = blocks.CharBlock(required=True)
    url = models.URLField()

class HomePage(Page):
    intro_de = RichTextField(default='')
    intro_fr = RichTextField(default='')
    intro = TranslatedField(
        'intro_de',
        'intro_fr',
    )

    body_de = RichTextField(default='')
    body_fr = RichTextField(default='')
    body = TranslatedField(
        'body_de',
        'body_fr',
    )

    infos_de = StreamField([
        ('info', InfoBlock())
    ], null=True, blank=True)
    infos_fr = StreamField([
        ('info', InfoBlock())
    ], null=True, blank=True)
    infos = TranslatedField(
        'infos_de',
        'infos_fr',
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro_de', classname="full"),
        FieldPanel('intro_fr', classname="full"),
        FieldPanel('body_de', classname="full"),
        FieldPanel('body_fr', classname="full"),
        StreamFieldPanel('infos_de'),
        StreamFieldPanel('infos_fr'),
    ]
