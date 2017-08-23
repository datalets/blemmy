# -*- coding: utf-8 -*-

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from .models import (
    Datasource,
    Category,
    Produce,
    Label,
    Region,
    Farm,
)

class FarmModelAdmin(ModelAdmin):
    model = Farm
    menu_icon = 'radio-full'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('title', 'region', 'updated')
    search_fields = ('title', 'about', 'person')

modeladmin_register(FarmModelAdmin)

class ProduceModelAdmin(ModelAdmin):
    model = Produce
    menu_icon = 'radio-empty'
    menu_order = 210
    add_to_settings_menu = False
    exclude_from_explorer = True

modeladmin_register(ProduceModelAdmin)

class CategoryModelAdmin(ModelAdmin):
    model = Category
    menu_icon = 'radio-empty'
    menu_order = 1000
    add_to_settings_menu = True
    exclude_from_explorer = True

modeladmin_register(CategoryModelAdmin)

class LabelModelAdmin(ModelAdmin):
    model = Label
    menu_icon = 'radio-empty'
    menu_order = 1010
    add_to_settings_menu = True
    exclude_from_explorer = True

modeladmin_register(LabelModelAdmin)

class RegionModelAdmin(ModelAdmin):
    model = Region
    menu_icon = 'radio-empty'
    menu_order = 1020
    add_to_settings_menu = True
    exclude_from_explorer = True

modeladmin_register(RegionModelAdmin)

class DatasourceModelAdmin(ModelAdmin):
    model = Datasource
    menu_icon = 'radio-empty'
    menu_order = 1030
    add_to_settings_menu = True
    exclude_from_explorer = True
    list_display = ('title', 'notes', 'homepage')

modeladmin_register(DatasourceModelAdmin)
