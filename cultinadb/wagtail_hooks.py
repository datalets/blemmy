# -*- coding: utf-8 -*-

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

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

######################################################
########## Settings Menu Permanent Daten #############
######################################################

class MenueModelAdmin(ModelAdmin):
    model = Menue
    menu_icon = 'plus'

class IngredientsModelAdmin(ModelAdmin):
    model = Ingredients
    menu_icon = 'snippet'

class MyModels(ModelAdminGroup):
    menu_label = 'LaCULTina'
    menu_icon = 'folder-open-inverse'
    menu_order = 200
    items = (WochenModelAdmin, MenueModelAdmin, IngredientsModelAdmin)

modeladmin_register(MyModels)
