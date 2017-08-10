
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

######################################################
#################### Ingredient #####################
######################################################

@register_model_chooser
class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    picture_url = models.URLField(blank=True)
    translate_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

######################################################
####################### Menu ########################
######################################################

@register_model_chooser
class Menu(models.Model):
    title = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    MENUTYPE = (
        ('Gericht', 'Gericht'),
        ('Suppe', 'Suppe'),
        ('Dessert', 'Dessert'),
    )
    type_of_dish_quantity = models.CharField(
        max_length=20, choices=MENUTYPE,
        blank=True, null=True, verbose_name='Art der Teller')
    Ingredient = StreamField([
        ('zutaten', ModelChooserBlock('cultinadb.Ingredient')),
    ])
    steps = StreamField([
        ('paragraph', TextBlock()),
    ])
    is_spicy = models.BooleanField(default=False, blank=True,
        verbose_name='Scharf')
    is_vegi = models.BooleanField(default=False,
        verbose_name='Vegi')

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('image'),
        StreamFieldPanel('Ingredient'),
        StreamFieldPanel('steps',
            # heading="Vorbereitung",
            classname="col12",
        ),
        FieldPanel('type_of_dish_quantity', classname="col4"),
        FieldPanel('is_vegi', classname="col2"),
        FieldPanel('is_spicy', classname="col2"),
    ]

    def __str__(self):
        return self.title

######################################################
####################### Woche ########################
######################################################

YEARS = (
    ('2017', 2017),
    # ('2018', 2018),
)
WEEKS = (
    ('01',1),('02',2),('03',3),('04',4),('05',5),('06',6),
    ('07',7),('08',8),('09',9),('10',10),('11',11),('12',12),
    ('13',13),('14',14),('15',15),('16',16),('17',17),('18',18),
    ('19',19),('20',20),('21',21),('22',22),('23',23),('24',24),
    ('25',25),('26',26),('27',27),('28',28),('29',29),('30',30),
    ('31',31),('32',32),('33',33),('34',34),('35',35),('36',36),
    ('37',37),('38',38),('39',39),('40',40),('41',41),('42',42),
    ('43',43),('44',44),('45',45),('46',46),('47',47),('48',48),
    ('49',49),('50',50),('51',51),('52',52),('53',53),
)
DAYS = (
    ('Montag',1),
    ('Dienstag',2),
    ('Mittwoch',3),
    ('Donnerstag',4),
    ('Freitag',5),
)

class Week(models.Model):
    year = models.IntegerField(verbose_name='Jahr', choices=YEARS,
        null=True)
    week = models.SmallIntegerField(verbose_name='Woche' ,choices=WEEKS,
        null=True)
    dishes_sp = StreamField([
        ('menu', ModelChooserBlock('cultinadb.Menu')) ], null=True)

    dishes_1 = StreamField([
        ('menu', ModelChooserBlock('cultinadb.Menu')) ], null=True)
    dishes_2 = StreamField([
        ('menu', ModelChooserBlock('cultinadb.Menu')) ], null=True)
    dishes_3 = StreamField([
        ('menu', ModelChooserBlock('cultinadb.Menu')) ], null=True)
    dishes_4 = StreamField([
        ('menu', ModelChooserBlock('cultinadb.Menu')) ], null=True)
    dishes_5 = StreamField([
        ('menu', ModelChooserBlock('cultinadb.Menu')) ], null=True)

    panels = [
        FieldPanel('year', classname="col3"),
        FieldPanel('week', classname="col9"),
        MultiFieldPanel(
            [ StreamFieldPanel('dishes_sp') ],
            heading="Wochenspezialität"
        )
    ]
    for d in DAYS:
        panels.append(
            MultiFieldPanel(
                [ StreamFieldPanel('dishes_' + str(d[1])) ],
                heading=d[0]
            )
        )

    def get_name(self):
        return "%d / %d" % (self.week, self.year)

    def __str__(self):
        return self.get_name()

    # api_fields = [
    #     APIField('title'),
    #     APIField('about'),
    #     APIField('image_thumb', serializer=ImageRenditionField('width-160', source='image')),
    #     APIField('image_full',  serializer=ImageRenditionField('width-800', source='image')),
    #     APIField('produce', serializer=ProduceRenditionField()),
    #     APIField('labels',  serializer=LabelRenditionField()),
    #     APIField('region',  serializer=RegionRenditionField()),
    #     APIField('distributors')
    # ]
