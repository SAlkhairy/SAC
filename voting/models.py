# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Max
from django.utils import timezone
from accounts.models import Profile, College
from .managers import YearQuerySet

city_choices = (
    ('', 'عامة'),
    ('R', 'الرياض'),
    ('J', 'جدة'),
    ('A', 'الأحساء'),
    )


class SACYear(models.Model):
    start_date = models.DateTimeField("تاريخ البداية")
    end_date = models.DateTimeField("تاريخ النهاية")
    election_nomination_start_datetime = models.DateTimeField("تاريخ بداية الترشيحات")
    election_nomination_end_datetime = models.DateTimeField("تاريخ نهاية الترشيحات")
    election_nomination_announcement_datetime = models.DateTimeField("تاريخ إعلان الترشيحات", null=True)
    election_vote_start_datetime = models.DateTimeField("تاريخ بداية التصويت", null=True, blank=True)
    election_vote_end_datetime = models.DateTimeField("تاريخ نهاية التصويت", null=True, blank=True)
    objects = YearQuerySet.as_manager()

    class Meta:
        verbose_name = 'السنة الأكاديمية'
        verbose_name_plural = "السنوات الأكاديمية"

    def get_next_year_name(self):
        return "%s-%s" % (self.start_date.year + 1, self.end_date.year + 1)

    def is_nomination_open(self):
        # If no election nomination start was specified, let's
        # consider the elections closed.  Otherwise, respect the
        # specified time.
        return self.election_nomination_start_datetime and \
               self.election_nomination_end_datetime and \
               self.election_nomination_start_datetime < timezone.now() and \
               self.election_nomination_end_datetime > timezone.now()

    def is_announcement_due(self):
        # If no announcement date is specified,
        # we'll consider the announcement not due;
        # so that, during nominations, non-rejected nominees (all of them)
        # will not appear until the proper date.
        return self.election_nomination_announcement_datetime and \
            self.election_nomination_announcement_datetime < timezone.now()

    def has_voting_started(self):
        if not self.election_vote_start_datetime:
            return
        else:
            return self.election_vote_start_datetime > timezone.now()

    def has_voting_closed(self):
        if not self.election_vote_end_datetime:
            return
        else:
            return timezone.now() > self.election_vote_end_datetime

    def is_voting_open(self):
        # If no election voting start is specified, the voting is
        # always closed.
        return self.has_voting_started() and \
               not self.has_voting_closed()

    def __unicode__(self):
        return "%s-%s" % (self.start_date.year, self.end_date.year)


class Position(models.Model):
    title = models.CharField("اسم المنصب",
                             max_length=55)
    entity_choices = (
        ('club', 'نادي الطلاب'),
        ('council', 'المجلس الطلابي الاستشاري'),
        )
    entity = models.CharField("اسم المنصب",
                              default="club",
                              max_length=50,
                              choices=entity_choices)
    city = models.CharField("المدينة", max_length=1, blank=True,
                            default="", choices=city_choices)
    colleges_allowed_to_vote = models.ManyToManyField(College,
                                                      verbose_name="الكليات المسموحة بالتصويت",
                                                      related_name='voting_positions')
    colleges_allowed_to_nominate = models.ManyToManyField(College,
                                                          verbose_name="الكليات المسموحة بالترشيح",
                                                          related_name='nomination_positions')
    note = models.TextField("ملاحظة", blank=True)
    submission_date = models.DateTimeField("تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)
    year = models.ForeignKey(SACYear, verbose_name="السنة")

    class Meta:
        verbose_name = 'المنصب'
        verbose_name_plural = 'المناصب'

    def get_total_votes(self):
        return self.votenomination_set.count()

    def get_blank_vote_count(self):
        return self.votenomination_set.filter(nomination_announcement__isnull=True).count()

    def get_blank_vote_percentage(self):
        total_count = self.get_total_votes()
        if not total_count:
            return 0
        blank_count = self.votenomination_set.filter(nomination_announcement__isnull=True).count()
        percentage = float(blank_count) / float(total_count) * 100
        return "{:.2f}".format(percentage)

    def get_winner(self):
        if self.nominationannouncement_set:
            return self.nominationannouncement_set.aggregate(Max('votenomination'))
        elif self.unelectedwinner_set:
            return self.unelectedwinner_set
        else:
            return None

    def is_elected(self):
        if self.nominationannouncement_set:
            return True

    def __unicode__(self):
        return self.title

class Nomination(models.Model):
    plan = models.FileField("الخطة")
    cv = models.FileField("السيرة الذاتية")
    certificates = models.FileField(null=True, verbose_name="الشهادات والمساهمات")
    gpa = models.FloatField("المعدل الجامعي", null=True)
    user = models.ForeignKey(User, verbose_name="المرشَّح")
    position = models.ForeignKey(Position, verbose_name="المنصب")
    is_rejected = models.BooleanField(default=False)
    submission_date = models.DateTimeField("تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)

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
    plan = models.FileField("الخطة", default="")
    cv = models.FileField("السيرة الذاتية", default="")
    user = models.ForeignKey(User, verbose_name="المرشَّح", default="")
    position = models.ForeignKey(Position, verbose_name="المنصب")

    class Meta:
        verbose_name = 'المرشحـ/ـة المؤهلـ/ـة'
        verbose_name_plural = 'المرشحون/المرشّحات المؤهلون/المؤهلات'

    def get_percentage(self):
        total_count = self.position.get_total_votes()
        if not total_count:
            return 0
        nomination_count = self.votenomination_set.count()
        percentage = float(nomination_count) / float(total_count) * 100
        return "{:.2f}".format(percentage)

    def __unicode__(self):
        try:
            name = self.user.profile.get_ar_full_name()
        except ObjectDoesNotExist:
            # If no profile
            name = self.user.username
        return "تأهُّل %s لِ%s" % (name, self.position.title)

class VoteNomination(models.Model):
    user = models.ForeignKey(User, verbose_name="المصوِّت")
    position = models.ForeignKey(Position, verbose_name="المنصب", null=True)
    nomination_announcement = models.ForeignKey(NominationAnnouncement, verbose_name="المرشَّح", null=True, blank=True)
    is_counted = models.BooleanField(default=True)
    submission_date = models.DateTimeField("تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)

    class Meta:
        verbose_name = 'صوت'
        verbose_name_plural = 'الأصوات'

    def __unicode__(self):
        if not self.nomination_announcement and \
           self.position:
            name = self.position.title
        elif self.nomination_announcement:
            try:
                name = self.nomination_announcement.user.profile.get_ar_full_name()
            except ObjectDoesNotExist:
                # If no profile
                name = self.nomination_announcement.user.username
        else:
            name = ""
        return "صوت لِ%s" % (name)

class UnelectedWinner(models.Model):
    user = models.ForeignKey(User, verbose_name="")
    position = models.ForeignKey(Position, verbose_name="المنصب")

class Referendum(models.Model):
    year = models.CharField("السنة", max_length=4)
    title = models.CharField("الموضوع", max_length=100)
    description = models.TextField("الوصف")
    opening_datetime = models.DateTimeField("تاريخ الابتداء")
    closing_datetime = models.DateTimeField("تاريخ الانتهاء")
    colleges_allowed = models.ManyToManyField(College, verbose_name="الكليات المسموحة")


class ReferendumFigure(models.Model):
    referendum = models.ForeignKey(Referendum, verbose_name="الاستفتاء")
    figure = models.ImageField(u"الصورة")

class VoteReferendum (models.Model):
    user = models.ForeignKey(User, verbose_name="المصوِّت")
    referendum = models.ForeignKey(Referendum, verbose_name="الاستفتاء")
    submission_date = models.DateTimeField("تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)
