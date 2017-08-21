# -*- coding: utf-8 -*-

from wagtail.api.v2.endpoints import BaseAPIEndpoint
from wagtail.api.v2.filters import FieldsFilter, OrderingFilter, SearchFilter
from wagtail.api.v2.serializers import BaseSerializer

from .models import Farm, Produce, Label, Datasource

class DatasourceAPIEndpoint(BaseAPIEndpoint):
    base_serializer_class = BaseSerializer
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    listing_default_fields = BaseAPIEndpoint.listing_default_fields + ['title', 'homepage']
    name = 'datasources'
    model = Datasource

class LabelAPIEndpoint(BaseAPIEndpoint):
    base_serializer_class = BaseSerializer
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    listing_default_fields = BaseAPIEndpoint.listing_default_fields + ['title', 'homepage', 'imageurl']
    name = 'labels'
    model = Label

class FarmsAPIEndpoint(BaseAPIEndpoint):
    base_serializer_class = BaseSerializer
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    listing_default_fields = BaseAPIEndpoint.listing_default_fields + ['title', 'about', 'image_thumb']
    nested_default_fields = BaseAPIEndpoint.nested_default_fields + ['title']
    name = 'farms'
    model = Farm

class ProduceAPIEndpoint(BaseAPIEndpoint):
    base_serializer_class = BaseSerializer
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    listing_default_fields = BaseAPIEndpoint.listing_default_fields + ['name', 'about', 'image_thumb']
    name = 'produce'
    model = Produce

def register_endpoints(api_router):
    api_router.register_endpoint('datasources', DatasourceAPIEndpoint)
    api_router.register_endpoint('labels', LabelAPIEndpoint)
    api_router.register_endpoint('farms', FarmsAPIEndpoint)
    api_router.register_endpoint('produce', ProduceAPIEndpoint)
