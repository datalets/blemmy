from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from .api import api_router

urlpatterns = [
    url(r'^api/v2/', api_router.urls),
]
