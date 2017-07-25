
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.api.fields import ImageRenditionField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.api import APIField

######################################################
####################### Menue ########################
######################################################

class TypeOfDish(models.Model):
    _type = models.CharField(max_length=255,
        verbose_name='Art der Nahrung',
        help_text=_('Gericht, Suppe, Dessert'))

    def __str__(self):
        return self._type

class Menue(models.Model):
    title = models.CharField(max_length=255)
    picture_url = models.URLField(blank=True)
    type_of_dish = models.ForeignKey(TypeOfDish,
        null=True, blank=True, on_delete=models.PROTECT)
    step_1 = models.CharField(max_length=500)
    step_2 = models.CharField(max_length=500)
    step_3 = models.CharField(max_length=500)
    step_4 = models.CharField(max_length=500)
    is_spicy = models.BooleanField(default=False,
        verbose_name='Scharf',
        help_text=_('Ist diese Gericht Scharf?'))
    is_vegi = models.BooleanField(default=False,
        verbose_name='Vegi',
        help_text=_('Ist diese Gericht Vegi?'))

    def __str__(self):
        return self.title

######################################################
#################### Ingredients #####################
######################################################

class Ingredients(models.Model):
    name = models.CharField(max_length=255)
    picture_url = models.URLField(blank=True)
    translate_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

######################################################
####################### Woche ########################
######################################################

class M_Jahr(models.Model):
    jahr = models.CharField(max_length=4,
    help_text=_('2017, 2018, 2019, 2020...'))
    def __str__(self):
        return self.jahr
class M_Woche(models.Model):
    woche = models.CharField(max_length=2,
    help_text=_('01, 02, 03, 04, 05, 06...'))
    def __str__(self):
        return self.woche
class M_Tag(models.Model):
    tag = models.CharField(max_length=2,
    help_text=_('Mo, Di, Mi, Do, Fr, Sa'))
    def __str__(self):
        return self.tag

class Wochen(models.Model):
    jahr = models.ForeignKey(M_Jahr,
        null=True, blank=True, on_delete=models.PROTECT)
    woche = models.ForeignKey(M_Woche,
        null=True, blank=True, on_delete=models.PROTECT)
    tag = models.ForeignKey(M_Tag,
        null=True, blank=True, on_delete=models.PROTECT)
    menu_1 = models.ForeignKey(Menue,
        null=True, blank=True, on_delete=models.PROTECT, related_name="menu_1")
    menu_2 = models.ForeignKey(Menue,
        null=True, blank=True, on_delete=models.PROTECT, related_name="menu_2")
    menu_3 = models.ForeignKey(Menue,
        null=True, blank=True, on_delete=models.PROTECT, related_name="menu_3")
    menu_4 = models.ForeignKey(Menue,
        null=True, blank=True, on_delete=models.PROTECT, related_name="menu_4")
    wochen_spezialitaet = models.ForeignKey(Menue,
        null=True, blank=True, on_delete=models.PROTECT, related_name="wochen_spezialitaet")
    tages_suppe = models.ForeignKey(Menue,
        null=True, blank=True, on_delete=models.PROTECT, related_name="tages_suppe")
    tages_dessert = models.ForeignKey(Menue,
        null=True, blank=True, on_delete=models.PROTECT, related_name="tages_dessert")

    panels = [
        FieldPanel('jahr', classname="col4"),
        FieldPanel('woche', classname="col4"),
        FieldPanel('tag', classname="col4"),
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
        return self.tag

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
