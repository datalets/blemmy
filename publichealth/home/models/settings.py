# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from wagtail.contrib.settings.models import BaseSetting, register_setting

@register_setting
class DataletsSettings(BaseSetting):
    feedback_question = models.TextBlock(
        help_text='Send us a question')
    feedback_status = models.IntegerField(
        choices=(
            (1, _':-('),
            (2, _':-|'),
            (3, _':-)'),
            (4, _':-D'),
        ), help_text='How are you enjoying Wagtail?'
    )
    feedback_comment = models.TextBlock(
        help_text='Any general feedback')
    class Meta:
        verbose_name = 'Datalets'

@receiver(pre_save, sender=DataletsSettings)
def handle_save_settings(sender, **kwargs):
    send_mail("Response from Wagtail",
        "%d\n--\n%s\n--\n%s" % (
            sender.feedback_status,
            sender.feedback_question,
            sender.feedback_comment,
        ), "wagtail@datalets.ch",
        [ "support@datalets.ch" ]
    )
