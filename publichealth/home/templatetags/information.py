# -*- coding: utf-8 -*-
from django import template
from django.utils import translation

from ..models.snippets import Contact

register = template.Library()

# Contact information (footer)
@register.inclusion_tag('tags/contact_info.html')
def contact_info():
    return {
        'contact': Contact.objects.last(),
    }

# Contact form (footer)
@register.inclusion_tag('tags/contact_form.html')
def contact_form():
    return {
        'contact': Contact.objects.last(),
    }
