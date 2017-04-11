# -*- coding: utf-8 -*-

from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)

from django.db.models import CharField
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailforms.models import (
    AbstractEmailForm, AbstractFormField
)

from ..util import TranslatedField

class ContactFormField(AbstractFormField):
    page = ParentalKey('ContactForm', related_name='form_fields')

class ContactForm(AbstractEmailForm):
    title_fr = CharField(max_length=255, default="")
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

    thanks_de = RichTextField(default='', blank=True)
    thanks_fr = RichTextField(default='', blank=True)
    trans_thanks = TranslatedField(
        'thanks_de',
        'thanks_fr',
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro_de', classname="full"),
        FieldPanel('thanks_de', classname="full"),
        FieldPanel('title_fr', classname="full"),
        FieldPanel('intro_fr', classname="full"),
        FieldPanel('thanks_fr', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    parent_page_types = ['home.ArticleIndexPage']
    class Meta:
        verbose_name = "Formular"
