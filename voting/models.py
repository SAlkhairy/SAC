# -*- coding: utf-8  -*-

from __future__ import unicode_literals


from django.db import models

from accounts.models import Profile, College

# Create your models here.



class SACYear(models.Model):
    start_date = models.DateTimeField("تاريخ البداية")
    end_date = models.DateTimeField("تاريخ النهاية")
    election_nomination_start_datetime = models.DateTimeField("تاريخ بداية الترشيحات")
    election_nomination_end_datetime = models.DateTimeField("تاريخ نهاية الترشيحات")
    election_vote_start_datetime = models.DateTimeField("تاريخ بداية التصويت")
    election_vote_end_datetime = models.DateTimeField("تاريخ نهاية التصويت")


class Position(models.Model):
    title = models.CharField("اسم المنصب")
    colleges_allowed_to_vote = models.ManyToManyField(College, "الكليات المسموحة بالتصويت")
    colleges_allowed_to_nominate = models.ManyToManyField(College, "الكليات المسموحة بالترشيح")
    submission_date = models.DateTimeField("تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)
    year = models.ForeignKey(SACYear, "السنة", max_length=4)


class Nomination(models.Model):
    plan = models.FileField("الخطة")
    cv = models.FileField("السيرة الذاتية")
    user = models.ForeignKey(Profile, "المرشح")
    position = models.ForeignKey(Position, "المنصب")
    submission_date = models.DateTimeField("تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)


class VoteNomination(models.Model):
    user = models.ForeignKey(Profile, "المصوت")
    nomination = models.ForeignKey(Nomination, "المرشح")
    submission_date = models.DateTimeField("تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)


class Referendum(models.Model):
    year = models.CharField("السنة",)
    title = models.CharField("الموضوع", max_length=100)
    description = models.TextField("الوصف", )
    opening_datetime = models.DateTimeField("تاريخ الابتداء",)
    closing_datetime = models.DateTimeField("تاريخ الانتهاء",)
    colleges_allowed = models.ManyToManyField(College, "الكليات المسموحة")


class ReferendumFigure(models.Model):
    referendum = models.ForeignKey(Referendum, "الاستفتاء",)


class VoteReferendum (models.Model):
    user = models.ForeignKey(Profile, "المصوت",)
    referendum = models.ForeignKey(Referendum, "الاستفتاء")
    submission_date = models.DateTimeField("تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)
