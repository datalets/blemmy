# -*- coding: utf-8 -*-

from wagtail.api.v2.endpoints import BaseAPIEndpoint
from wagtail.api.v2.filters import FieldsFilter, OrderingFilter, SearchFilter
from wagtail.api.v2.serializers import BaseSerializer

from .models import Farm, Produce, Region, Label, Datasource

class FarmsAPIEndpoint(BaseAPIEndpoint):
    base_serializer_class = BaseSerializer
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    listing_default_fields = BaseAPIEndpoint.listing_default_fields + ['title', 'about', 'image']
    nested_default_fields = BaseAPIEndpoint.nested_default_fields + ['title']
    name = 'farms'
    model = Farm

class ProduceAPIEndpoint(BaseAPIEndpoint):
    base_serializer_class = BaseSerializer
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    name = 'produce'
    model = Produce

def register_endpoints(api_router):
    api_router.register_endpoint('farms', FarmsAPIEndpoint)
    api_router.register_endpoint('produce', ProduceAPIEndpoint)
