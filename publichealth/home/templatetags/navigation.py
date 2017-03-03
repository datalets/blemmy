# -*- coding: utf-8 -*-
from django import template
from django.utils import translation

register = template.Library()

# Language switcher
@register.inclusion_tag('home/templates/tags/language.html', takes_context=True)
def language_switcher(context):
    return {
        'languages': [ { 'code': 'de', 'title': 'De' }, { 'code': 'fr', 'title': 'Fr' } ],
        'currentlangcode': translation.get_language(),
        'request': context['request'],
    }
