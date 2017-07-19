# -*- coding: utf-8 -*-

from wagtail.contrib.wagtailapi.endpoints import BaseAPIEndpoint
from wagtail.contrib.wagtailapi.serializers import BaseSerializer
from wagtail.contrib.wagtailapi.filters import FieldsFilter, OrderingFilter, SearchFilter
from wagtail.contrib.wagtailapi.pagination import WagtailPagination

from .models import Farm

class FarmSerializer(BaseSerializer):
    pass

class FarmsAPIEndpoint(BaseAPIEndpoint):
    base_serializer_class = FarmSerializer
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    extra_api_fields = [
        'name',
        'about',
        'website',
        'longitude',
        'latitude',
        'image',
        'updated',
        'region',
    ]
    name = 'farms'
    model = Farm
