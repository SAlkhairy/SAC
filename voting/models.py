# -*- coding: utf-8  -*-

from __future__ import unicode_literals

from django.db import models

from accounts.models import Profile, College

# Create your models here.



class SACYear(models.Model):
    start_date = models.DateTimeField(u"تاريخ البداية")
    end_date = models.DateTimeField(u"تاريخ النهاية")
    election_nomitation_start_datetime = models.DateTimeField(u"تاريخ بداية الترشيحات")
    election_nomitation_end_datetime = models.DateTimeField(u"تاريخ نهاية الترشيحات")
    election_vote_start_datetime = models.DateTimeField(u"تاريخ بداية التصويت")
    election_vote_end_datetime = models.DateTimeField(u"تاريخ نهاية التصويت")


class Position(models.Model):
    title = models.CharField(u"اسم المنصب")
    colleges_allowed_to_vote = models.ManyToManyField(College, u"الكليات المسموحة بالتصويت")
    colleges_allowed_to_nominate = models.ManyToManyField(College, u"الكليات المسموحة بالترشيح")
    submission_date = models.DateTimeField(u"تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل", auto_now=True, null=True)
    year = models.CharField(u"السنة", max_length=4)


class Nomination(models.Model):
    plan = models.FileField(u"الخطة") #right?
    cv = models.FileField(u"السيرة الذاتية") #right?
    user = models.OneToOneField(Profile, u"المرشِّح")
    position = models.ForeignKey(Position, u"المنصب")
    submission_date = models.DateTimeField(u"تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل", auto_now=True, null=True)


class VoteNomination(models.Model):
    user = models.OneToOneField(Profile, u"المصوِّت")
    nomination = models.ForeignKey(Nomination, u"المرشّح")
    submission_date = models.DateTimeField(u"تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل", auto_now=True, null=True)


class Referendum(models.Model):
    year = models.CharField(u"السنة",)
    title = models.CharField(u"الموضوع", max_length=100)
    description = models.TextField(u"الوصف", )
    opening_datetime = models.DateTimeField(u"تاريخ الابتداء",)
    closing_datetime = models.DateTimeField(u"تاريخ الانتهاء",)
    colleges_allowed = models.ManyToManyField(College, u"الكليات المسموحة")


class ReferendumFigure(models.Model):
    referendum = models.OneToOneField(Referendum, u"الاستفتاء",)


class VoteReferendum (models.Model):
    user = models.OneToOneField(Profile, u"المصوٍّت",)
    referendum = models.ForeignKey(Referendum, u"الاستفتاء")
    submission_date = models.DateTimeField(u"تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل", auto_now=True, null=True)
