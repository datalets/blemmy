# -*- coding: utf-8 -*-
from django import template
from django.utils import translation

from ..models.snippets import Contact, SocialContact

register = template.Library()

# Contact information (footer)
@register.inclusion_tag('tags/contact_info.html')
def contact_info():
    return {
        'contact': Contact.objects.last(),
        'socials': SocialContact.objects.all()
    }

# Contact form (footer)
@register.inclusion_tag('tags/footer_form.html')
def footer_form():
    if Contact.objects.last():
        return {
            'form': Contact.objects.last().contact_form,
        }

# Contact links (header)
@register.inclusion_tag('tags/contact_links.html')
def contact_links():
    return {
        'contact': Contact.objects.last(),
        'socials': SocialContact.objects.all()
    }

# Styled contact name (header)
@register.inclusion_tag('tags/contact_name.html')
def contact_name():
    return {
        'contact': Contact.objects.last(),
    }
