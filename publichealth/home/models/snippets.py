# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailsnippets.models import register_snippet

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, PageChooserPanel

from .forms import ContactForm
from ..util import TranslatedField

# List of supported social networks
SOCIAL_NETWORK_SUPPORTED = (
    ('twitter', 'Twitter'),
    ('facebook', 'Facebook'),
)

@register_snippet
class SocialContact(models.Model):
    """
    Adds contact options through social networks
    """
    network = models.CharField(max_length=16, default="twitter",
        choices=SOCIAL_NETWORK_SUPPORTED)
    profile = models.CharField(max_length=255, default="",
        help_text="Name of the account, e.g. @myaccount, or full URL")
    panels = [
        FieldPanel('network'),
        FieldPanel('profile'),
    ]
    social_networks = dict(SOCIAL_NETWORK_SUPPORTED)
    def network_title(self):
        return self.social_networks[self.network]
    def network_url(self):
        if '://' in self.profile:
            return self.profile
        if self.network == 'twitter':
            return "https://twitter.com/%s" % self.profile
        elif self.network == 'facebook':
            return "https://facebook.com/%s" % self.profile
        return "#"
    def __str__(self):
        return "%s" % self.network

@register_snippet
class Contact(models.Model):
    """
    Defines contact options for the organisation, usually shown in footer
    """
    title = models.CharField(max_length=255, default="")
    title_fr = models.CharField(max_length=255, default="")
    trans_title = TranslatedField(
        'title',
        'title_fr',
    )
    address = models.TextField(default="", blank=True)
    phone = models.CharField(max_length=40, default="")
    email = models.EmailField(max_length=100, default="")
    www = models.URLField(null=True, blank=True)

    map_url = models.URLField(null=True, blank=True,
        help_text="Optional link of address to mapping provider")
    analytics = models.CharField(max_length=60, default="", blank=True,
        help_text="Optional web analytics property code")

    contact_form = models.ForeignKey(
        'home.ContactForm',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = Page.content_panels + [
        FieldPanel('title_fr'),
        FieldPanel('address'),
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('www'),
        FieldPanel('map_url'),
        FieldPanel('analytics'),
        PageChooserPanel('contact_form', 'home.ContactForm'),
    ]

    def phone_link(self):
        return 'tel:%s' % self.phone.replace(' ', '')
    def email_link(self):
        return 'mailto:%s' % self.email
    def www_domain(self):
        return self.www.replace('http://', '').replace('https://', '')
    def is_google_analytics(self):
        return self.analytics.startswith('UA-')
    def get_piwik_analytics(self):
        # When formatted as "server|site_id", assume Piwik
        if not '|' in self.analytics: return False
        sa = self.analytics.split('|')
        return { 'server': sa[0], 'site': sa[1] }
    def trans_title_styled(self):
        v = self.trans_title.split(' ')
        if len(v) != 3: return v
        return "<strong>%s %s</strong> %s" % tuple(v)
    def __str__(self):
        return self.trans_title
