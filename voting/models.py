# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from accounts.models import Profile, College
from .managers import YearQuerySet

class SACYear(models.Model):
    start_date = models.DateTimeField(verbose_name="تاريخ البداية")
    end_date = models.DateTimeField(verbose_name="تاريخ النهاية")
    election_nomination_start_datetime = models.DateTimeField(verbose_name="تاريخ بداية الترشيحات")
    election_nomination_end_datetime = models.DateTimeField(verbose_name="تاريخ نهاية الترشيحات")
    election_nomination_announcement_datetime = models.DateTimeField(verbose_name="تاريخ إعلان الترشيحات", null=True)
    election_vote_start_datetime = models.DateTimeField(verbose_name="تاريخ بداية التصويت")
    election_vote_end_datetime = models.DateTimeField(verbose_name="تاريخ نهاية التصويت")
    objects = YearQuerySet.as_manager()

    class Meta:
        verbose_name = 'السنة الأكاديمية'
        verbose_name_plural = "السنوات الأكاديمية"

    def get_next_year_name(self):
        return "%s-%s" % (self.start_date.year + 1, self.end_date.year + 1)

    def is_nomination_open(self):
        # If no election nomination end was specified, let's consider
        # the elections open forever.  Otherwise, respect the
        # specified time.
        if not self.election_nomination_end_datetime:
            return True
        else:
            return self.election_nomination_end_datetime > timezone.now()

    def is_announcement_due(self):
        # If no announcement date is specified,
        # we'll consider the announcement not due;
        # so that, during nominations, non-rejected nominees (all of them)
        # will not appear until the proper date.
        if not self.election_nomination_announcement_datetime:
            return False
        else:
            return self.election_nomination_announcement_datetime < timezone.now()

    def is_voting_open(self):
        # If no election voting start is specified,
        # the voting is always closed.
        if not self.election_vote_start_datetime:
            return False
        else:
            return self.election_vote_end_datetime > timezone.now()

    def __unicode__(self):
        return "%s-%s" % (self.start_date.year, self.end_date.year)



class Position(models.Model):
    title = models.CharField(verbose_name="اسم المنصب",
                             max_length=50)
    entity_choices = (
        ('club', 'نادي الطلاب'),
        ('council', 'المجلس الطلابي الاستشاري'),
        )
    entity = models.CharField(verbose_name="اسم المنصب",
                              default="club",
                              max_length=50,
                              choices=entity_choices)
    colleges_allowed_to_vote = models.ManyToManyField(College,
                                                      verbose_name="الكليات المسموحة بالتصويت",
                                                      related_name='vote')
    colleges_allowed_to_nominate = models.ManyToManyField(College,
                                                          verbose_name="الكليات المسموحة بالترشيح",
                                                          related_name='nominate')
    submission_date = models.DateTimeField(verbose_name="تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField(verbose_name="تاريخ التعديل", auto_now=True, null=True)
    year = models.ForeignKey(SACYear, verbose_name="السنة",)

    class Meta:
        verbose_name = 'المنصب'
        verbose_name_plural = 'المناصب'

    def __unicode__(self):
        return self.title

class Nomination(models.Model):
    plan = models.FileField(verbose_name="الخطة")
    cv = models.FileField(verbose_name="السيرة الذاتية")
    certificates = models.FileField(null=True, verbose_name="الشهادات والمساهمات")
    gpa = models.FloatField(verbose_name="المعدل الجامعي", null=True)
    user = models.ForeignKey(User, verbose_name="المرشَّح")
    position = models.ForeignKey(Position, verbose_name="المنصب")
    is_rejected = models.BooleanField(default=False)
    submission_date = models.DateTimeField(verbose_name="تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField(verbose_name="تاريخ التعديل", auto_now=True, null=True)

    class Meta:
        verbose_name = 'المرشحـ/ـة'
        verbose_name_plural = 'المرشحون/المرشّحات'

    def __unicode__(self):
        try:
            name = self.user.profile.get_ar_full_name()
        except ObjectDoesNotExist:
            # If no profile
            name = self.user.username
        return "ترشّح %s لِ%s" % (name, self.position.title)

class NominationAnnouncement(models.Model):
    plan = models.FileField(verbose_name="الخطة", default="")
    cv = models.FileField(verbose_name="السيرة الذاتية", default="")
    user = models.ForeignKey(User, verbose_name="المرشَّح", default="")
    position = models.ForeignKey(Position, verbose_name="المنصب")

    class Meta:
        verbose_name = 'المرشحـ/ـة المؤهلـ/ـة'
        verbose_name_plural = 'المرشحون/المرشّحات المؤهلون/المؤهلات'

    def __unicode__(self):
        try:
            name = self.user.profile.get_ar_full_name()
        except ObjectDoesNotExist:
            # If no profile
            name = self.user.username
        return "تأهُّل %s لِ%s" % (name, self.position.title)


class VoteNomination(models.Model):
    user = models.ForeignKey(User, verbose_name="المصوِّت")
    nomination = models.ForeignKey(Nomination, verbose_name="المرشَّح")
    submission_date = models.DateTimeField(verbose_name="تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField(verbose_name="تاريخ التعديل", auto_now=True, null=True)


class Referendum(models.Model):
    year = models.CharField(verbose_name="السنة", max_length=4)
    title = models.CharField(verbose_name="الموضوع", max_length=100)
    description = models.TextField(verbose_name="الوصف", )
    opening_datetime = models.DateTimeField(verbose_name="تاريخ الابتداء",)
    closing_datetime = models.DateTimeField(verbose_name="تاريخ الانتهاء",)
    colleges_allowed = models.ManyToManyField(College, verbose_name="الكليات المسموحة")


class ReferendumFigure(models.Model):
    referendum = models.ForeignKey(Referendum, verbose_name="الاستفتاء")
    figure = models.ImageField(u"الصورة")

class VoteReferendum (models.Model):
    user = models.ForeignKey(User, verbose_name="المصوِّت",)
    referendum = models.ForeignKey(Referendum, verbose_name="الاستفتاء")
    submission_date = models.DateTimeField(verbose_name="تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField(verbose_name="تاريخ التعديل", auto_now=True, null=True)


