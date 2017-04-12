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
    intro = RichTextField(default='', blank=True)
    thanks = RichTextField(default='', blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('thanks', classname="full"),
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
