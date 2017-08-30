
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.blocks import TextBlock
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.api.fields import ImageRenditionField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.api import APIField
from wagtailmodelchooser import register_model_chooser
from wagtailmodelchooser.blocks import ModelChooserBlock
from django_countries.fields import CountryField

######################################################
#################### Ingredient ######################
######################################################

@register_model_chooser
class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    picture_url = models.URLField(blank=True)
    translate_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    api_fields = [
        APIField('name'),
        APIField('picture_url'),
        APIField('translate_url'),
    ]

class IngredientChooserBlock(ModelChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                'name': value.name,
                'picture': value.picture_url,
                'translate': value.translate_url
            }
######################################################
####################### Menu #########################
######################################################

@register_model_chooser
class Menu(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True, max_length=255)
    MENUTYPE = (
        ('Gericht', 'Gericht'),
        ('Suppe', 'Suppe'),
        ('Dessert', 'Dessert'),
    )
    type_of_dish_quantity = models.CharField(
        max_length=20, choices=MENUTYPE,
        blank=True, null=True, verbose_name='Art der Teller')
    ingredient = StreamField([
        ('zutaten', IngredientChooserBlock('cultinadb.Ingredient')) ],
        null=True, verbose_name='', blank=True)
    zutaten_beschreibung = models.TextField(verbose_name='Zutaten Beschreibung', blank=True)
    is_spicy = models.BooleanField(default=False, blank=True,
        verbose_name='Scharf')
    is_vegi = models.BooleanField(default=False,
        verbose_name='Vegi')
    steps = StreamField([
        ('Schritt', TextBlock())
        ], null=True, verbose_name='Vorbereitungsschritte', blank=True)

    panels = [
        FieldPanel('title', classname="col7"),
        FieldPanel('price', classname="col2"),
        FieldPanel('type_of_dish_quantity', classname="col3"),
        FieldPanel('image', classname="col7"),
        FieldPanel('is_vegi', classname="col2"),
        FieldPanel('is_spicy', classname="col3"),
        FieldPanel('zutaten_beschreibung', classname="col7"),
        MultiFieldPanel(
            [ StreamFieldPanel('ingredient') ],
            heading="Zutaten", classname="col5"
        ),
        StreamFieldPanel('steps', classname="col12"),
    ]

    def __str__(self):
        return self.title

class WeekChooserBlock(ModelChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            ingredient = value.ingredient
            steps = str(value.steps)
            return {
                'id': value.id,
                'title': value.title,
                'picture': value.image,
                'price': value.price,
                'type_of_dish_quantity': value.type_of_dish_quantity,
                'ingredients': ingredient.stream_block.get_api_representation(ingredient, context=context),
                'zutaten_beschreibung': value.zutaten_beschreibung,
                'is_spicy': value.is_spicy,
                'is_vegi': value.is_vegi,
                'steps': steps
            }

######################################################
####################### Woche ########################
######################################################

YEARS = (
    (2017, 2017),
    # (2018, 2018),
)
WEEKS = (
    (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),
    (7,7),(8,8),(9,9),(10,10),(11,11),(12,12),
    (13,13),(14,14),(15,15),(16,16),(17,17),(18,18),
    (19,19),(20,20),(21,21),(22,22),(23,23),(24,24),
    (25,25),(26,26),(27,27),(28,28),(29,29),(30,30),
    (31,31),(32,32),(33,33),(34,34),(35,35),(36,36),
    (37,37),(38,38),(39,39),(40,40),(41,41),(42,42),
    (43,43),(44,44),(45,45),(46,46),(47,47),(48,48),
    (49,49),(50,50),(51,51),(52,52),(53,53),
)
DAYS = (
    ('Montag',1),
    ('Dienstag',2),
    ('Mittwoch',3),
    ('Donnerstag',4),
    ('Freitag',5),
)

class Week(models.Model):
    country = CountryField(
        verbose_name='Land', blank=True, null=True, blank_label='Wochenspezialität ist aus ...')
    year = models.IntegerField(verbose_name='Jahr', choices=YEARS,
        null=True)
    week = models.SmallIntegerField(verbose_name='Woche' ,choices=WEEKS,
        null=True)
    dishes_sp = StreamField([
        ('menu', WeekChooserBlock('cultinadb.Menu')) ],
        null=True, verbose_name='', blank=True)
    monday = StreamField([
        ('menu', WeekChooserBlock('cultinadb.Menu')) ],
        null=True, verbose_name='', blank=True)
    tuesday = StreamField([
        ('menu', WeekChooserBlock('cultinadb.Menu')) ],
        null=True, verbose_name='', blank=True)
    wednesday = StreamField([
        ('menu', WeekChooserBlock('cultinadb.Menu')) ],
        null=True, verbose_name='', blank=True)
    thursday = StreamField([
        ('menu', WeekChooserBlock('cultinadb.Menu')) ],
        null=True, verbose_name='', blank=True)
    friday = StreamField([
        ('menu', WeekChooserBlock('cultinadb.Menu')) ],
        null=True, verbose_name='', blank=True)

    panels = [
        FieldPanel('country', classname="col6"),
        FieldPanel('year', classname="col4"),
        FieldPanel('week', classname="col2"),
        MultiFieldPanel(
            [ StreamFieldPanel('dishes_sp') ],
            heading="Wochenspezialität", classname="col6"
        ),
        MultiFieldPanel(
            [ StreamFieldPanel('monday') ],
            heading="Montag", classname="col6"
        ),
        MultiFieldPanel(
            [ StreamFieldPanel('tuesday') ],
            heading="Dienstag", classname="col6"
        ),
        MultiFieldPanel(
            [ StreamFieldPanel('wednesday') ],
            heading="Mittwoch", classname="col6"
        ),
        MultiFieldPanel(
            [ StreamFieldPanel('thursday') ],
            heading="Donnerstag", classname="col6"
        ),
        MultiFieldPanel(
            [ StreamFieldPanel('friday') ],
            heading="Freitag", classname="col6"
        ),
    ]

    def get_name(self):
        for d in DAYS:
            return "%d / %d" % (self.week, self.year)

    def __str__(self):
        return self.get_name()

    api_fields = [
        APIField('country'),
        APIField('year'),
        APIField('week'),
        APIField('dishes_sp'),
        APIField('monday'),
        APIField('tuesday'),
        APIField('wednesday'),
        APIField('thursday'),
        APIField('friday'),
    ]
