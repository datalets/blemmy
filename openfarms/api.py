from wagtail.api.v2.router import WagtailAPIRouter
from .endpoints import FarmsAPIEndpoint

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('farms', FarmsAPIEndpoint)
