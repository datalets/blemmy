# -*- coding: utf-8 -*-

from wagtail.api.v2.endpoints import BaseAPIEndpoint

from .models import Week, Ingredient, Menu

class WeekAPIEndpoint(BaseAPIEndpoint):
    model = Week
    listing_default_fields = BaseAPIEndpoint.listing_default_fields + ['year', 'week']


class IngredientsAPIEndpoint(BaseAPIEndpoint):
    model = Ingredient

def register_endpoints(api_router):
    api_router.register_endpoint('week', WeekAPIEndpoint)
    api_router.register_endpoint('ingredients', IngredientsAPIEndpoint)
