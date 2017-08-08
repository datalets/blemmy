
from django.db import models
from django.utils.translation import ugettext_lazy as _

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
#################### Ingredients #####################
######################################################

@register_model_chooser
class Ingredients(models.Model):
    name = models.CharField(max_length=255)
    picture_url = models.URLField(blank=True)
    translate_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

######################################################
####################### Menue ########################
######################################################

class Menue(models.Model):

    title = models.CharField(max_length=255, verbose_name='Titel')
    picture_url = models.URLField(blank=True, verbose_name='Bild URL')
    ARTDERNAHRUNG = (
        ('Gericht', 'Gericht'),
        ('Suppe', 'Suppe'),
        ('Dessert', 'Dessert'),
        ('...', '...'),
    )
    type_of_dish_quantity = models.CharField(max_length=2, choices=ARTDERNAHRUNG,
        blank=True, verbose_name='Art der Nahrung')
    zutaten = StreamField([
        ('zutaten', ModelChooserBlock('cultinadb.Ingredients')),
    ])
    schritte_1 = models.TextField(max_length=500, blank=True)
    schritte_2 = models.TextField(max_length=500, blank=True)
    schritte_3 = models.TextField(max_length=500, blank=True)
    schritte_4 = models.TextField(max_length=500, blank=True)
    is_spicy = models.BooleanField(default=False, blank=True,
        verbose_name='Scharf')
    is_vegi = models.BooleanField(default=False,
        verbose_name='Vegi')

    panels = [
        FieldPanel('title', classname="col12"),
        FieldPanel('picture_url', classname="col8"),
        FieldPanel('type_of_dish_quantity', classname="col4"),
        StreamFieldPanel('zutaten', 'cultinadb.Ingredients'),
        MultiFieldPanel([
            FieldPanel('schritte_1'),
            FieldPanel('schritte_2'),
            FieldPanel('schritte_3'),
            FieldPanel('schritte_4'),
        ],
        heading="Vorbereitung",
        classname="col12",
        ),
        FieldPanel('is_vegi', classname="col2"),
        FieldPanel('is_spicy', classname="col2"),
    ]

    def __str__(self):
        return self.title

######################################################
####################### Woche ########################
######################################################

class Wochen(models.Model):
    JAHR = (
        ('2017', '2017'),
        # ('2018', '2018'),
    )
    WOCHE = (
        ('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),
        ('07','07'),('08','08'),('09','09'),('10','10'),('11','11'),('12','12'),
        ('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),
        ('19','19'),('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),
        ('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),
        ('31','31'),('32','32'),('33','33'),('34','34'),('35','35'),('36','36'),
        ('37','37'),('38','38'),('39','39'),('40','40'),('41','41'),('42','42'),
        ('43','43'),('44','44'),('45','45'),('46','46'),('47','47'),('48','48'),
        ('49','49'),('50','50'),('51','51'),('52','52'),('53','53'),
    )
    TAG = (
        ('Mo','Mo'),
        ('Di','Di'),
        ('Mi','Mi'),
        ('Do','Do'),
        ('Fr','Fr'),
    )
    jahr_quantity = models.CharField(max_length=2, verbose_name='Jahr', choices=JAHR,
        null=True)
    woche_quantity = models.CharField(max_length=2, verbose_name='Woche' ,choices=WOCHE,
        null=True)
    tag_quantity = models.CharField(max_length=2, verbose_name='Tag', choices=TAG,
        null=True)
    menu_1 = models.ForeignKey(Menue,
        null=True, on_delete=models.PROTECT, related_name="menu_1+")
    menu_2 = models.ForeignKey(Menue,
        null=True, on_delete=models.PROTECT, related_name="menu_2+")
    menu_3 = models.ForeignKey(Menue,
        null=True, on_delete=models.PROTECT, related_name="menu_3+")
    menu_4 = models.ForeignKey(Menue,
        null=True, on_delete=models.PROTECT, related_name="menu_4+")
    wochen_spezialitaet = models.ForeignKey(Menue,
        null=True, verbose_name='Wochenspezialität', on_delete=models.PROTECT, related_name="wochen_spezialitaet+")
    tages_suppe = models.ForeignKey(Menue,
        null=True, verbose_name='Tagessuppe', on_delete=models.PROTECT, related_name="tages_suppe+")
    tages_dessert = models.ForeignKey(Menue,
        null=True, verbose_name='Tagesdessert', on_delete=models.PROTECT, related_name="tages_dessert+")

    panels = [
        FieldPanel('jahr_quantity', classname="col4"),
        FieldPanel('woche_quantity', classname="col4"),
        FieldPanel('tag_quantity', classname="col4"),
        MultiFieldPanel([
            FieldPanel('menu_1'),
            FieldPanel('menu_2'),
            FieldPanel('menu_3'),
            FieldPanel('menu_4'),
        ],
        heading="Menüs",
        classname="col12",
        ),
        FieldPanel('wochen_spezialitaet', classname="col12"),
        FieldPanel('tages_suppe', classname="col12"),
        FieldPanel('tages_dessert', classname="col12"),
    ]

    def __str__(self):
        return self.tag_quantity

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
