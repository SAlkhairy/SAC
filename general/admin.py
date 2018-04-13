# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from . import models


def make_read(ModelAdmin, request, queryset):
    queryset.update(is_read=True)
make_read.short_description = "تغيير حالة الرسائل المختارة إلى 'مقروءة'"

def make_unread(ModelAdmin, request, queryset):
    queryset.update(is_read=False)
make_unread.short_description = "تغيير حالة الرسائل المختارة إلى 'غير مقروءة'"

class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ['city', 'college', 'year', 'is_read']
    list_display = ['title', 'city', 'college', 'year','is_read']
    search_fields = ['title']

    actions = [make_read, make_unread]

class NewsAdmin(admin.ModelAdmin):
    list_filter = ['year']
    list_display = ['title', 'submission_date']

class DebateQAdmin(admin.ModelAdmin):
    list_filter = ['year', 'is_read']
    list_display = ['question', 'year','is_read']
    search_fields = ['question']

    actions = [make_read, make_unread]


admin.site.register(models.Feedback, FeedbackAdmin)
admin.site.register(models.NewsItem, NewsAdmin)
admin.site.register(models.DebateQ, DebateQAdmin)


