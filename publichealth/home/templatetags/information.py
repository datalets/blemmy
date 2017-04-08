# -*- coding: utf-8 -*-
from django import template
from django.utils import translation

from ..snippets import Contact

register = template.Library()

# Contact information (footer)
@register.inclusion_tag('tags/contact_info.html')
def contact_info():
    return {
        'contact': Contact.objects.first(),
    }
