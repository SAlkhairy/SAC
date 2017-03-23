# -*- coding: utf-8  -*-

from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from userena.models import UserenaBaseProfile



# Create your models here.


gender_choices = (
    ('F', 'طالبة'),
    ('M', 'طالب'),
)


college_choices = (
    ('M', 'كلية الطب'),
    ('A', 'كلية العلوم الطبية التطبيقية'),
    ('P', 'كلية الصيدلة'),
    ('D', 'كلية طب الأسنان'),
    ('B', 'كلية العلوم و المهن الصحية'),
    ('N', 'كلية التمريض'),
    ('I', ' كلية الصحة العامة والمعلوماتية الصحية'),
)



city_choices = (
    ('R', 'الرياض'),
    ('J', 'جدة'),
    ('A', 'الأحساء'),
)


class College(models.Model):
    name = models.CharField(max_length=1, choices=college_choices, verbose_name=u"الاسم")
    city = models.CharField(max_length=1, choices=city_choices, verbose_name=u"المدينة")
    gender = models.CharField(max_length=1, choices=gender_choices, verbose_name=u"الجنس")

    def __unicode__(self):
        return u"%s (%s - %s)" % (self.get_name_display(),
                                       self.get_section_display(),
                                       self.get_gender_display())

    class Meta:
        # For the admin interface.
        verbose_name = "كلية"
        verbose_name_plural = "الكليات"



class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User)
    ar_name = models.TextField(max_length=100, verbose_name="الاسم بالعربي")
    en_name = models.TextField(max_length=100, verbose_name="الاسم بالإنجليزي")
    college = models.ForeignKey(College, verbose_name="الكلية")
    city = models.CharField(max_length=1, choices=city_choices, verbose_name="المدينة")
    gender = models.CharField(max_length=1, choices=gender_choices, verbose_name="الجنس")
    mobile_number = models.CharField(verbose_name="رقم الجوال", max_length=14)
    student_id = models.IntegerField(unique=True, verbose_name="الرقم الجامعي")
    submission_date = models.DateTimeField(verbose_name=u"تاريخ التسجيل", auto_now_add=True)
    modification_date = models.DateTimeField(verbose_name="تاريخ التعديل", auto_now=True, null=True,)

