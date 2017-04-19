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

from puput.models import EntryPage

from ..util import TranslatedField

class InfoBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    photo = ImageChooserBlock(required=True)
    summary = blocks.RichTextBlock(required=True)
    action = blocks.CharBlock(required=False)
    url = blocks.URLBlock(required=False)

class ArticleIndexPage(Page):
    title_fr = models.CharField(max_length=255, default="")
    trans_title = TranslatedField(
        'title',
        'title_fr',
    )

    intro_de = RichTextField(default='', blank=True)
    intro_fr = RichTextField(default='', blank=True)
    trans_intro = TranslatedField(
        'intro_de',
        'intro_fr',
    )

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro_de'),
        FieldPanel('title_fr'),
        FieldPanel('intro_fr'),
        ImageChooserPanel('feed_image'),
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
        'home.ContactForm'
    ]
    class Meta:
        verbose_name = "Rubrik"

class ArticlePage(Page):
    title_fr = models.CharField(max_length=255, default="")
    trans_title = TranslatedField(
        'title',
        'title_fr',
    )

    intro_de = RichTextField(default='', blank=True)
    intro_fr = RichTextField(default='', blank=True)
    trans_intro = TranslatedField(
        'intro_de',
        'intro_fr',
    )

    body_de = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('section', blocks.CharBlock(classname="full title")),
        ('info', InfoBlock()),
    ], null=True, blank=True)
    body_fr = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('section', blocks.CharBlock(classname="full title")),
        ('info', InfoBlock()),
    ], null=True, blank=True)
    trans_body = TranslatedField(
        'body_de',
        'body_fr',
    )

    date = models.DateField("Date", null=True, blank=True)

    on_homepage = models.BooleanField(default=False, verbose_name="Featured",
        help_text="Auf der Frontpage anzeigen")

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
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
        ImageChooserPanel('feed_image'),
    ]
    promote_panels = [
        InlinePanel('related_links', label="Links"),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('on_homepage'),
        ], heading="Veröffentlichung"),
        MultiFieldPanel(Page.promote_panels, "Einstellungen"),
    ]

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

class HomePage(Page):
    intro_de = RichTextField(default='')
    intro_fr = RichTextField(default='')
    trans_intro = TranslatedField(
        'intro_de',
        'intro_fr',
    )

    body_de = RichTextField(default='', blank=True)
    body_fr = RichTextField(default='', blank=True)
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

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro_de', classname="full"),
            FieldPanel('body_de', classname="full"),
            StreamFieldPanel('infos_de'),
        ], heading="Deutsch"),
            MultiFieldPanel([
            FieldPanel('intro_fr', classname="full"),
            FieldPanel('body_fr', classname="full"),
            StreamFieldPanel('infos_fr'),
        ], heading="Français"),
    ]

    @property
    def featured(self):
        # Get list of live pages that are descendants of this page
        articles = ArticlePage.objects.live() #.descendant_of(self)
        articles = articles.filter(on_homepage=True)
        # Order by most recent date first
        #articles = articles.order_by('-date')
        return articles[:4]

    @property
    def newsfeed(self):
        # Get list of latest news
        # TODO: fetch children of 'News (DE)'
        entries = EntryPage.objects.live().descendant_of(self)
        # Order by most recent date first
        entries = entries.order_by('-date')
        return entries[:4]

    def get_context(self, request):
        # Update template context
        context = super(HomePage, self).get_context(request)
        context['featured'] = self.featured
        context['newsfeed'] = self.newsfeed
        return context

    parent_page_types = []
    class Meta:
        verbose_name = "Frontpage"
