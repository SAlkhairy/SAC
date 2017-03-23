# -*- coding: utf-8  -*-

from __future__ import unicode_literals


from django.db import models

from accounts.models import Profile, College

# Create your models here.



class SACYear(models.Model):
    start_date = models.DateTimeField(verbose_name="تاريخ البداية")
    end_date = models.DateTimeField(verbose_name="تاريخ النهاية")
    election_nomination_start_datetime = models.DateTimeField(verbose_name="تاريخ بداية الترشيحات")
    election_nomination_end_datetime = models.DateTimeField(verbose_name="تاريخ نهاية الترشيحات")
    election_vote_start_datetime = models.DateTimeField(verbose_name="تاريخ بداية التصويت")
    election_vote_end_datetime = models.DateTimeField(verbose_name="تاريخ نهاية التصويت")


class Position(models.Model):
    title = models.CharField(verbose_name="اسم المنصب",
                             max_length=50)
    colleges_allowed_to_vote = models.ManyToManyField(College,
                                                      verbose_name="الكليات المسموحة بالتصويت",
                                                      related_name='vote')
    colleges_allowed_to_nominate = models.ManyToManyField(College,
                                                          verbose_name="الكليات المسموحة بالترشيح",
                                                          related_name='nominate')
    submission_date = models.DateTimeField(verbose_name="تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField(verbose_name="تاريخ التعديل", auto_now=True, null=True)
    year = models.ForeignKey(SACYear, verbose_name="السنة", max_length=4)


class Nomination(models.Model):
    plan = models.FileField(verbose_name="الخطة")
    cv = models.FileField(verbose_name="السيرة الذاتية")
    user = models.ForeignKey(Profile, verbose_name="المرشح")
    position = models.ForeignKey(Position, verbose_name="المنصب")
    submission_date = models.DateTimeField(verbose_name="تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField(verbose_name="تاريخ التعديل", auto_now=True, null=True)


class VoteNomination(models.Model):
    user = models.ForeignKey(Profile, verbose_name="المصوِّت")
    nomination = models.ForeignKey(Nomination, "المرشَّح")
    submission_date = models.DateTimeField("تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)


class Referendum(models.Model):
    year = models.CharField(verbose_name="السنة", max_length=4)
    title = models.CharField(verbose_name="الموضوع", max_length=100)
    description = models.TextField(verbose_name="الوصف", )
    opening_datetime = models.DateTimeField(verbose_name="تاريخ الابتداء",)
    closing_datetime = models.DateTimeField(verbose_name="تاريخ الانتهاء",)
    colleges_allowed = models.ManyToManyField(College, verbose_name="الكليات المسموحة")


class ReferendumFigure(models.Model):
    referendum = models.ForeignKey(Referendum, verbose_name="الاستفتاء")


class VoteReferendum (models.Model):
    user = models.ForeignKey(Profile, verbose_name="المصوِّت",)
    referendum = models.ForeignKey(Referendum, verbose_name="الاستفتاء")
    submission_date = models.DateTimeField(verbose_name="تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField(verbose_name="تاريخ التعديل", auto_now=True, null=True)
