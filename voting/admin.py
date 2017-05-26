# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import admin
from . import forms, models
from .utils import BASIC_SEARCH_FIELDS


def make_rejected(ModelAdmin, request, queryset):
    queryset.update(is_rejected=True)
make_rejected.short_description = "رفض المرشحـ/ين المختار/ين"

def create_nomination_announcement(ModelAdmin, request, queryset):
    for nomination in queryset:
        models.NominationAnnouncement.objects.create(user=nomination.user, position=nomination.position)
create_nomination_announcement.short_description =\
    "إنشاء حساب المرشحين/المرشحات المؤهلين/المؤهلات"

def make_uncounted(ModelAdmin, request, queryset):
    queryset.update(is_counted=False)
make_uncounted.short_description = "استبعاد الأصوات المختارة"


class NominationAdmin(admin.ModelAdmin):
    list_filter = ['position__city', 'position__entity', 'is_rejected']
    list_display = ['__unicode__', 'cv', 'plan', 'certificates', 'gpa','is_rejected']
    search_fields = ['position__title'] + BASIC_SEARCH_FIELDS

    actions = [make_rejected, create_nomination_announcement]

class PositionAdmin(admin.ModelAdmin):
    list_filter = ['entity', 'year']

class VoteNominationAdmin(admin.ModelAdmin):
    list_filter = ['nomination_announcement__position',
                   'nomination_announcement__position__entity']
    list_display = ['get_student_id', 'is_counted']
    search_fields = ['position__title'] + BASIC_SEARCH_FIELDS

    actions = [make_uncounted]

    def get_student_id(self, obj):
        try:
            return obj.user.profile.student_id
        except ObjectDoesNotExist:
            return

class UnelectedWinnerAdmin(admin.ModelAdmin):
    form = forms.UnelectedWinnerForm
    search_fields = ['position__title'] + BASIC_SEARCH_FIELDS
    list_filter = ['position__city', 'position__entity']

admin.site.register(models.Nomination, NominationAdmin)
admin.site.register(models.NominationAnnouncement)
admin.site.register(models.Position, PositionAdmin)
admin.site.register(models.VoteNomination, VoteNominationAdmin)
admin.site.register(models.UnelectedWinner, UnelectedWinnerAdmin)
admin.site.register(models.SACYear)
