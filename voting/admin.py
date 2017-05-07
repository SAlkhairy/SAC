# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django.contrib import admin
from voting.models import Position, SACYear, Nomination,\
                          NominationAnnouncement, VoteNomination

def make_rejected(ModelAdmin, request, queryset):
    queryset.update(is_rejected=True)
make_rejected.short_description = "رفض المرشحـ/ين المختار/ين"

def create_nomination_announcement(ModelAdmin, request, queryset):
    for nomination in queryset:
        NominationAnnouncement.objects.create(user=nomination.user, position=nomination.position)
create_nomination_announcement.short_description =\
    "إنشاء حساب المرشحين/المرشحات المؤهلين/المؤهلات"

class NominationAdmin(admin.ModelAdmin):
    list_filter = ['position', 'is_rejected']
    list_display = ['__unicode__', 'cv', 'plan', 'certificates', 'gpa','is_rejected']
    search_fields = ['position__title', 'user__username',
                     'user__email', 'user__profile__ar_first_name',
                     'user__profile__ar_middle_name',
                     'user__profile__ar_last_name',
                     'user__profile__en_first_name',
                     'user__profile__en_middle_name',
                     'user__profile__en_last_name',
                     'user__profile__student_id',
                     'user__profile__mobile_number']

    actions = [make_rejected, create_nomination_announcement]

class PositionAdmin(admin.ModelAdmin):
    list_filter = ['entity', 'year']

class VoteNominationAdmin(admin.ModelAdmin):
    list_filter = ['nomination_announcement__position',
                   'nomination_announcement__position__entity']

admin.site.register(Nomination, NominationAdmin)
admin.site.register(NominationAnnouncement)
admin.site.register(Position, PositionAdmin)
admin.site.register(VoteNomination, VoteNominationAdmin)
admin.site.register(SACYear)
