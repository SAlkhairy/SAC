# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

from django.core.mail import EmailMessage

from accounts.models import Profile, College, college_choices, city_choices
from voting.models import SACYear

class Feedback(models.Model):
    city = models.CharField("المدينة", max_length=1, choices=city_choices)
    college = models.ForeignKey(College, verbose_name="الكلية", null=True)
    email = models.EmailField(max_length=70, blank=True)
    title = models.CharField("العنوان", max_length=100, blank=False)
    description = models.TextField("الوصف", blank=False)
    picture = models.FileField("صورة", blank=True, null=True)
    submission_date = models.DateTimeField("تاريخ الرفع", auto_now_add=True)
    year = models.ForeignKey(SACYear, verbose_name="السنة")
    is_read = models.BooleanField("مقروءة؟", default=False)

    class Meta:
        verbose_name = 'المقترَح/الملاحظة'
        verbose_name_plural = 'المقترحات/الملاحظات'

class NewsItem(models.Model):
    title = models.CharField("العنوان", max_length=100, blank=False)
    body = models.TextField("العرض", blank=False)
    picture = models.FileField("صورة", blank=True, null=True)
    submission_date = models.DateTimeField("تاريخ النشر", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)
    year = models.ForeignKey(SACYear, verbose_name="السنة")

    class Meta:
        verbose_name = 'الخبر'
        verbose_name_plural = 'الأخبار'

class DebateQ(models.Model):
    question = models.TextField("السؤال", blank=False)
    submission_date = models.DateTimeField("تاريخ الرفع", auto_now_add=True)
    year = models.ForeignKey(SACYear, verbose_name="السنة")
    is_read = models.BooleanField("مقروءة؟", default=False)

    class Meta:
        verbose_name = 'سؤال المناظرة'
        verbose_name_plural = 'أسئلة المناظرة'

    def email_SAC(self):
        msg = EmailMessage(
                               'سؤال للمناظرة | بوابة ترابط',
                               '' + self.question + '',
                               'noreply@trabdportal.com',
                               ['sac@ksau-hs.edu.sa', ]
                          )
        msg.content_subtype = "html"
        msg.send()
