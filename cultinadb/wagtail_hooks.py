# -*- coding: utf-8 -*-

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from .models import (
    Wochen,
    M_Jahr,
    M_Woche,
    M_Tag,
    Menue,
    TypeOfDish,
    Ingredients,
)

######################################################
#################### Sidebar Menu ####################
######################################################

class WochenModelAdmin(ModelAdmin):
    model = Wochen
    menu_icon = 'radio-full'
    menu_order = 200
    exclude_from_explorer = True

modeladmin_register(WochenModelAdmin)

######################################################
########## Settings Menu Permanent Daten #############
######################################################

class MenueModelAdmin(ModelAdmin):
    model = Menue
    menu_icon = 'radio-empty'
    menu_order = 210
    add_to_settings_menu = True

modeladmin_register(MenueModelAdmin)

class IngredientsModelAdmin(ModelAdmin):
    model = Ingredients
    menu_icon = 'radio-empty'
    menu_order = 210
    add_to_settings_menu = True

modeladmin_register(IngredientsModelAdmin)

class TypeOfDishModelAdmin(ModelAdmin):
    model = TypeOfDish
    menu_icon = 'radio-empty'
    menu_order = 210
    add_to_settings_menu = True

modeladmin_register(TypeOfDishModelAdmin)

class M_WocheModelAdmin(ModelAdmin):
    model = M_Woche
    menu_icon = 'radio-empty'
    menu_order = 210
    add_to_settings_menu = True

modeladmin_register(M_WocheModelAdmin)

class M_TagModelAdmin(ModelAdmin):
    model = M_Tag
    menu_icon = 'radio-empty'
    menu_order = 210
    add_to_settings_menu = True

modeladmin_register(M_TagModelAdmin)

class M_JahrModelAdmin(ModelAdmin):
    model = M_Jahr
    menu_icon = 'radio-empty'
    menu_order = 210
    add_to_settings_menu = True

modeladmin_register(M_JahrModelAdmin)
