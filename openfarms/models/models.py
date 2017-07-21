# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.api.fields import ImageRenditionField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.api import APIField

from djmoney.models.fields import MoneyField

from .serializers import ProduceRenditionField, LabelRenditionField, RegionRenditionField

class Datasource(models.Model):
    title = models.CharField(max_length=255)
    homepage = models.URLField()
    feed = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    api_fields = [
        'title', 'homepage',
    ]
    def __str__(self):
        return self.title

class Label(models.Model):
    title = models.CharField(max_length=255)
    about = models.TextField(blank=True)
    imageurl = models.URLField(blank=True)
    def __str__(self):
        return self.title

class Region(models.Model):
    title = models.CharField(max_length=255)
    imageurl = models.URLField(blank=True)
    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=255)
    info = models.TextField(blank=True)
    imageurl = models.URLField(blank=True)
    parent = models.ManyToManyField("self", blank=True,
        help_text=_('Specify if another category is a parent of this one (e.g. Fruits > Apples)'))
    verbose_name_plural = 'Categories'
    def __str__(self):
        return self.title

class Farm(models.Model):
    title = models.CharField(max_length=255, unique=True)
    about = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    person = models.CharField(max_length=255, blank=True,
        verbose_name=_('Name of responsible contact'))
    phone = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    latitude = models.CharField(max_length=50, blank=True)

    updated = models.DateTimeField(auto_now=True, editable=False)
    published = models.DateTimeField(auto_now_add=True, editable=False)

    is_producer = models.BooleanField(default=True,
        verbose_name='Producer',
        help_text=_('Is this a producer (and not only distributor)?'))
    distributors = models.ManyToManyField("self", blank=True)

    labels = models.ManyToManyField(Label, blank=True)
    region = models.ForeignKey(Region,
        null=True, blank=True, on_delete=models.PROTECT)
    datasource = models.ForeignKey(Datasource,
        null=True, blank=True, on_delete=models.PROTECT)

    panels = [
        FieldPanel('title'),
        FieldPanel('about'),
        ImageChooserPanel('image'),
        MultiFieldPanel([
            FieldPanel('person'),
            FieldPanel('phone'),
            FieldPanel('mobile'),
            FieldPanel('email'),
            FieldPanel('website'),
            FieldPanel('address'),
            FieldPanel('longitude'),
            FieldPanel('latitude'),
        ],
        heading="Contact",
        classname="collapsible collapsed",
        ),
        MultiFieldPanel([
            FieldPanel('region'),
            FieldPanel('labels'),
        ],
        heading="Details",
        classname="col5",
        ),
        MultiFieldPanel([
            FieldPanel('is_producer'),
            FieldPanel('distributors'),
            FieldPanel('datasource'),
        ],
        heading="Connections",
        classname="col7",
        ),
    ]

    api_fields = [
        APIField('title'), APIField('about'),
        APIField('image_thumb', serializer=ImageRenditionField('width-160', source='image')),
        APIField('image_full',  serializer=ImageRenditionField('width-800', source='image')),
        APIField('produce', serializer=ProduceRenditionField()),
        APIField('labels',  serializer=LabelRenditionField()),
        APIField('region',  serializer=RegionRenditionField()),
        APIField('distributors')
    ]
    api_meta_fields = [
        'person', 'phone', 'mobile',
        'email', 'website', 'address',
        'longitude', 'latitude',
        'is_producer',
    ]

    def __str__(self):
        return self.title

class Produce(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField(blank=True)

    category = models.ForeignKey(Category,
        null=True, blank=True, on_delete=models.PROTECT)

    is_fresh = models.BooleanField(default=True,
        verbose_name='Fresh',
        help_text=_('This is a fresh product (i.e. unprocessed).'))
    is_glutenfree = models.BooleanField(default=True,
        verbose_name='Gluten-free',
        help_text=_('Check if this product is free of gluten.'))
    is_dairyfree = models.BooleanField(default=True,
        verbose_name='Dairy-free',
        help_text=_('Milk is not part of this produce.'))
    is_nutsfree = models.BooleanField(default=True,
        verbose_name='Nut-free',
        help_text=_('Nuts are not part of this produce.'))
    is_vegan = models.BooleanField(default=True,
        verbose_name='Vegan',
        help_text=_('This is not an animal product.'))

    QUANTITYCHOICE = (
        ('kg', 'Kilogram'),
        ('g',  'Gram'),
        ('l',  'Litre'),
        ('b',  'Bushel'),
    )
    price_quantity = models.CharField(max_length=2, choices=QUANTITYCHOICE)
    price_chf = MoneyField(max_digits=10, decimal_places=2, default_currency='CHF')

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    labels = models.ManyToManyField(Label, blank=True,
        help_text=_('What special modes of production were used.'))
    farms = models.ManyToManyField(Farm, blank=True, related_name='produce',
        help_text=_('Where is this produce available.'))

    panels = [
        FieldPanel('name'),
        FieldPanel('farms'),
        MultiFieldPanel([
            FieldPanel('category'),
            FieldPanel('about'),
            ImageChooserPanel('image'),
            FieldPanel('price_chf'),
            FieldPanel('price_quantity'),
        ],
        heading="Details",
        classname="col5",
        ),
        MultiFieldPanel([
            FieldPanel('is_fresh'),
            FieldPanel('is_glutenfree'),
            FieldPanel('is_dairyfree'),
            FieldPanel('is_nutsfree'),
            FieldPanel('is_vegan'),
            FieldPanel('labels'),
        ],
        heading="Features",
        classname="col7",
        ),
    ]

    api_fields = [
        APIField('name'),
        APIField('about'),
        APIField('category'),
        APIField('image_thumb', serializer=ImageRenditionField('width-160', source='image')),
        APIField('image_full',  serializer=ImageRenditionField('width-800', source='image')),
        APIField('labels'),
        APIField('farms'),
    ]
    api_meta_fields = [
        'is_fresh', 'is_glutenfree', 'is_dairyfree',
        'is_nutsfree', 'is_vegan',
    ]
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Produce'
