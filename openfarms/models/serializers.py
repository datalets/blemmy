# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from collections import OrderedDict
from rest_framework.fields import Field
from wagtail.wagtailimages.models import SourceImageIOError
from wagtail.api.v2.serializers import get_object_detail_url

def get_thumbnail(image):
    try:
        if image is None: return {}
        thumbnail = image.get_rendition('width-160')
        return OrderedDict([
            ('url', thumbnail.url),
            ('width', thumbnail.width),
            ('height', thumbnail.height),
        ])
    except SourceImageIOError:
        return OrderedDict([
            ('error', 'SourceImageIOError'),
        ])

class ProduceRenditionField(Field):
    def get_attribute(self, instance):
        return instance
    def to_representation(self, farm):
        d = []
        for produce in farm.produce.all():
            url = get_object_detail_url(self.context, type(produce), produce.pk)
            d.append(OrderedDict([
                ('name', produce.name),
                ('about', produce.about),
                ('thumb', get_thumbnail(produce.image)),
                ('detail_url', url)
            ]))
        return d

class LabelRenditionField(Field):
    def get_attribute(self, instance):
        return instance
    def to_representation(self, farm):
        d = []
        for label in farm.labels.all():
            d.append(OrderedDict([
                ('title', label.title),
                ('about', label.about),
                ('imageurl', label.imageurl),
            ]))
        return d

class RegionRenditionField(Field):
    def get_attribute(self, instance):
        return instance
    def to_representation(self, farm):
        return OrderedDict([
            ('title', farm.region.title),
            ('imageurl', farm.region.imageurl),
        ])
