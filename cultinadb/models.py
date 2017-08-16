
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.blocks import TextBlock, DateBlock
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.api.fields import ImageRenditionField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.api import APIField
from wagtailmodelchooser import register_model_chooser
from wagtailmodelchooser.blocks import ModelChooserBlock
from wagtailmodelchooser.edit_handlers import ModelChooserPanel
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

######################################################
####################### Menu #########################
######################################################

@register_model_chooser
class Menu(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)
    MENUTYPE = (
        ('Gericht', 'Gericht'),
        ('Suppe', 'Suppe'),
        ('Dessert', 'Dessert'),
    )
    type_of_dish_quantity = models.CharField(
        max_length=20, choices=MENUTYPE,
        blank=True, null=True, verbose_name='Art der Teller')
    Ingredient = StreamField([
        ('zutaten', ModelChooserBlock('cultinadb.Ingredient')) ],
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
        FieldPanel('type_of_dish_quantity', classname="col5"),
        FieldPanel('image', classname="col7"),
        FieldPanel('is_vegi', classname="col2"),
        FieldPanel('is_spicy', classname="col3"),
        FieldPanel('zutaten_beschreibung', classname="col7"),
        MultiFieldPanel(
            [ StreamFieldPanel('Ingredient') ],
            heading="Zutaten", classname="col5"
        ),
        StreamFieldPanel('steps', classname="col12"),
    ]

    def __str__(self):
        return self.title

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
        ('menu', ModelChooserBlock('cultinadb.Menu')) ],
        null=True, verbose_name='', blank=True)
    monday = StreamField([
        ('menu', ModelChooserBlock('cultinadb.Menu')) ],
        null=True, verbose_name='', blank=True)
    tuesday = StreamField([
        ('menu', ModelChooserBlock('cultinadb.Menu')) ],
        null=True, verbose_name='', blank=True)
    wednesday = StreamField([
        ('menu', ModelChooserBlock('cultinadb.Menu')) ],
        null=True, verbose_name='', blank=True)
    thursday = StreamField([
        ('menu', ModelChooserBlock('cultinadb.Menu')) ],
        null=True, verbose_name='', blank=True)
    friday = StreamField([
        ('menu', ModelChooserBlock('cultinadb.Menu')) ],
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
        APIField('year'),
        APIField('week'),
        APIField('dishes_sp'),
        APIField('monday'),
        APIField('tuesday'),
        APIField('wednesday'),
        APIField('thursday'),
        APIField('friday'),
    ]
