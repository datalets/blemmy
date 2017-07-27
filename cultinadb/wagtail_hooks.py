# -*- coding: utf-8 -*-

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from .models import (
    Wochen,
    Menue,
    Ingredients,
)

######################################################
#################### Sidebar Menu ####################
######################################################

class WochenModelAdmin(ModelAdmin):
    model = Wochen
    menu_icon = 'form'
    menu_order = 200
    exclude_from_explorer = True

modeladmin_register(WochenModelAdmin)

######################################################
########## Settings Menu Permanent Daten #############
######################################################

class MenueModelAdmin(ModelAdmin):
    model = Menue
    menu_icon = 'plus'
    menu_order = 210
    add_to_settings_menu = True

modeladmin_register(MenueModelAdmin)

class IngredientsModelAdmin(ModelAdmin):
    model = Ingredients
    menu_icon = 'snippet'
    menu_order = 210
    add_to_settings_menu = True

modeladmin_register(IngredientsModelAdmin)
