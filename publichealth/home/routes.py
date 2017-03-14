# -*- coding: utf-8 -*-

from datetime import date

from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route

class HomePage(RoutablePageMixin, Page):

    @route(r'^$')
    def home_page(self, request, *args, **kwargs):
        self.articles = self.get_articles()
        return Page.serve(self, request, *args, **kwargs)
