# -*- coding: utf-8 -*-
from django import template
from django.utils import translation

register = template.Library()

# Language switcher
@register.inclusion_tag('tags/language.html', takes_context=True)
def language_switcher(context):
    url = context['page'].url.split('/')
    if len(url) > 2 and len(url[1]) >= 2:
        url[1] = '$lang$'
        url = '/'.join(url)
    return {
        'languages': [
            { 'code': 'de', 'title': 'De', 'url': url.replace('$lang$','de') },
            { 'code': 'fr', 'title': 'Fr', 'url': url.replace('$lang$','fr') }
        ],
        'currentlangcode': translation.get_language(),
        'request': context['request'],
    }

@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page

def has_menu_children(page):
    return page.get_children().live().in_menu().exists()

# Retrieves the top menu items
@register.inclusion_tag('tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu().specific()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)
        menuitem.title = menuitem.trans_title
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        'request': context['request'],
    }

def menuitems_children(parent):
    menuitems_children = parent.get_children().live().in_menu().specific()
    for menuitem in menuitems_children:
        menuitem.title = menuitem.trans_title
    return menuitems_children

# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    return {
        'parent': parent,
        'menuitems_children': menuitems_children(parent),
        'request': context['request'],
    }

# Retrieves the footer menu items
@register.inclusion_tag('tags/footer_menu.html', takes_context=True)
def footer_menu(context, parent, calling_page=None):
    return {
        'calling_page': calling_page,
        'menuitems': menuitems_children(parent),
        'request': context['request'],
    }
