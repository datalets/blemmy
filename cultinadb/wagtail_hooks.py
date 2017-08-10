# -*- coding: utf-8 -*-

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from .models import (
    Week,
    Menu,
    Ingredient,
)

######################################################
#################### Sidebar Menu ####################
######################################################

class WeekModelAdmin(ModelAdmin):
    model = Week
    menu_icon = 'form'

######################################################
########## Settings Menu Permanent Daten #############
######################################################

class MenuModelAdmin(ModelAdmin):
    model = Menu
    menu_icon = 'plus'

class IngredientModelAdmin(ModelAdmin):
    model = Ingredient
    menu_icon = 'snippet'

class LaCultinaModels(ModelAdminGroup):
    menu_label = 'LaCULTina'
    menu_icon = 'folder-open-inverse'
    menu_order = 200
    items = (WeekModelAdmin, MenuModelAdmin, IngredientModelAdmin)

modeladmin_register(LaCultinaModels)
