from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
# API model
from wagtail.api import APIField

# Create your models here.

class FeedPage(Page):
    intro = RichTextField(blank=True)

    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    postdate = models.DateField(default='YYYY-MM-DD', blank=True)
    body = RichTextField(blank=True)

    api_fields = [
        # APIField('intro'),
        APIField('body'),
        # APIField('main_image'),
        # APIField('date'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('main_image'),
        FieldPanel('intro', classname="col7"),
        FieldPanel('postdate', classname="col5"),
        MultiFieldPanel([
                FieldPanel('body'),
            ],
            heading="Content",
            classname="collapsible collapsed col12",
    ),
    ]
    class Meta:
        verbose_name = "Feed Page"
