# -*- coding: utf-8  -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.




gender_choices = (
    ('F', u'طالبة'),
    ('M', u'طالب'),
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





class SACYear(models.Model):
    start_date = models.DateTimeField(u"تاريخ البداية")
    end_date = models.DateTimeField(u"تاريخ النهاية")
    election_nomitation_start_datetime = models.DateTimeField(u"تاريخ بداية الترشيحات")
    election_nomitation_end_datetime = models.DateTimeField(u"تاريخ نهاية الترشيحات")
    election_vote_start_datetime = models.DateTimeField(u"تاريخ بداية التصويت")
    election_vote_end_datetime = models.DateTimeField(u"تاريخ نهاية التصويت")



class Position(models.Model):
    title = models.CharField()
    colleges_allowed_to_vote=
    colleges_allowed_to_nomiate =
    submission_date = models.DateTimeField(u"تاريخ ال", auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, null=True)
    year = models.CharField()


###class Nomiation(models.Model):
    plan=()
    CV=()
    User=()
    Position=()
    submission_date = models.DateTimeField(u"تاريخ ال", auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, null=True)

class VoteNomition(models.Model):
    user=()
    Nomition=()
    submission_date = models.DateTimeField(u"تاريخ ال", auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, null=True)

class VoteReferendum (models.Model):
    User=()
    Referendum=()
    submission_date = models.DateTimeField(u"تاريخ ال", auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, null=True)
class Referendum(models.Model):
    year=()
    title=()
    description=()
    opening_datetime=()
    closing_datetime=()
    colleges_allowed=('M2M')

class ReferendumFigure(models.Model):
    referendum=()
