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
    ('M', u'كلية الطب'),
    ('A', u'كلية العلوم الطبية التطبيقية'),
    ('P', u'كلية الصيدلة'),
    ('D', u'كلية طب الأسنان'),
    ('B', u'كلية العلوم و المهن الصحية'),
    ('N', u'كلية التمريض'),
    ('I', u' كلية الصحة العامة والمعلوماتية الصحية'),
)



city_choices = (
    ('R', u'الرياض'),
    ('J', u'جدة'),
    ('A', u'الأحساء'),
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
        verbose_name = u"كلية"
        verbose_name_plural = u"الكليات"



class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User)
    ar_name = models.TextField()
    en_name = models.TextField()
    college = models.ForeignKey(College)
    city = models.CharField(max_length=1, choices=city_choices, verbose_name=u"المدينة")
    gender = models.CharField(max_length=1, choices=gender_choices, verbose_name=u"الجنس")
    mobile_number = models.CharField(max_length=12)
    email = models.EmailField(blank=False)
    student_id = models.IntegerField(unique=True)
    submission_date = models.DateTimeField(verbose_name=u"تاريخ التسجيل", auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, null=True,)

