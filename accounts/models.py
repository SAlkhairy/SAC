# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from userena.models import UserenaBaseProfile


gender_choices = (
    ('', '--'),
    ('F', 'طالبات'),
    ('M', 'طلاب'),
)

college_choices = (
    ('', '--'),
    ('M', 'كلية الطب'),
    ('A', 'كلية العلوم الطبية التطبيقية'),
    ('P', 'كلية الصيدلة'),
    ('D', 'كلية طب الأسنان'),
    ('B', 'كلية العلوم و المهن الصحية'),
    ('N', 'كلية التمريض'),
    ('I', ' كلية الصحة العامة والمعلوماتية الصحية'),
)

city_choices = (
    ('', '--'),
    ('R', 'الرياض'),
    ('J', 'جدة'),
    ('A', 'الأحساء'),
)

class College(models.Model):
    name = models.CharField("الاسم", max_length=1,
                            choices=college_choices)
    city = models.CharField("المدينة", max_length=1,
                            choices=city_choices)
    gender = models.CharField("الجنس", max_length=1,
                              choices=gender_choices)

    def __unicode__(self):
        return "%s (%s - %s)" % (self.get_name_display(),
                                 self.get_city_display(),
                                 self.get_gender_display())

    class Meta:
        # For the admin interface.
        verbose_name = "كلية"
        verbose_name_plural = "الكليات"

class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User, verbose_name="مستخدمـ/ـة")
    ar_first_name = models.CharField(u'الاسم الأول', max_length=30)
    ar_middle_name = models.CharField(u'الاسم الأوسط', max_length=30)
    ar_last_name = models.CharField('الاسم الأخير', max_length=30)
    en_first_name = models.CharField(u'الاسم الأول', max_length=30)
    en_middle_name = models.CharField('الاسم الأوسط', max_length=30)
    en_last_name = models.CharField(u'الاسم الأخير', max_length=30)
    college = models.ForeignKey(College, verbose_name="الكلية", null=True)
    city = models.CharField("المدينة", max_length=1, choices=city_choices)
    gender = models.CharField("الجنس", max_length=1, choices=gender_choices)
    mobile_number = models.CharField("رقم الجوال", max_length=14)
    student_id = models.IntegerField("الرقم الجامعي", unique=True, null=True)
    submission_date = models.DateTimeField("تاريخ التسجيل", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)

    def get_ar_full_name(self):
        ar_fullname = None
        try:
            # If the Arabic first name is missing, let's assume the
            # rest is also missing.
            if self.ar_first_name:
                ar_fullname = " ".join([self.ar_first_name,
                                        self.ar_middle_name,
                                        self.ar_last_name])
        except AttributeError: # If the user has their details missing
            pass

        return ar_fullname

    def get_en_full_name(self):
        en_fullname = None
        try:
            # If the English first name is missing, let's assume the
            # rest is also missing.
            if self.en_first_name:
                en_fullname = " ".join([self.en_first_name,
                                        self.en_middle_name,
                                        self.en_last_name])
        except AttributeError: # If the user has their details missing
            pass

        return en_fullname
