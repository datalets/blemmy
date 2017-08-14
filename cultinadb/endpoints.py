# -*- coding: utf-8 -*-

from wagtail.api.v2.endpoints import BaseAPIEndpoint
from wagtail.api.v2.filters import FieldsFilter, OrderingFilter, SearchFilter
from wagtail.api.v2.serializers import BaseSerializer

from .models import Week

class WeekAPIEndpoint(BaseAPIEndpoint):
    base_serializer_class = BaseSerializer
    filter_backends = [FieldsFilter, OrderingFilter, SearchFilter]
    name = 'week'
    model = Week

def register_endpoints(api_router):
    api_router.register_endpoint('week', WeekAPIEndpoint)
