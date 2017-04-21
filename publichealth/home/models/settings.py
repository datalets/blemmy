# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from wagtail.contrib.settings.models import BaseSetting, register_setting

@register_setting
class DataletsSettings(BaseSetting):
    feedback_question = models.TextField(
        help_text='Send us a question', blank=True)
    feedback_status = models.IntegerField(
        choices=(
            (1, ':-('),
            (2, ':-|'),
            (3, ':-)'),
            (4, ':-D'),
        ), blank=True, null=True,
        help_text='How are you enjoying Wagtail?'
    )
    feedback_comment = models.TextField(
        help_text='Any general feedback', blank=True)
    class Meta:
        verbose_name = 'Datalets'

@receiver(pre_save, sender=DataletsSettings)
def handle_save_settings(sender, instance, *args, **kwargs):
    if instance.feedback_status is not None:
        send_mail("Response from Wagtail",
            "%s\n--\n%s\n--\n%s" % (
                str(instance.feedback_status),
                instance.feedback_question,
                instance.feedback_comment,
            ), "wagtail@datalets.ch",
            [ "support@datalets.ch" ]
        )
        instance.feedback_status = None
        instance.feedback_question = ""
        instance.feedback_comment = ""
