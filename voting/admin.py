# -*- coding: utf-8  -*-
from __future__ import unicode_literals

from django.contrib import admin

from voting.models import Position, SACYear, Nomination

# Register your models here.

admin.site.register(SACYear)

admin.site.register(Position)



def make_rejected(ModelAdmin, request, queryset):
    queryset.update(is_rejected=True)
make_rejected.short_description = "رفض المرشحـ/ين المختار/ين"


class NominationAdmin(admin.ModelAdmin):
    list_filter = ['position', 'is_rejected']
    search_fields = ['position', 'is_rejected']
    actions = [make_rejected]

admin.site.register(Nomination, NominationAdmin)



