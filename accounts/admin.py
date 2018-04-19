from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from userena.admin import UserenaAdmin
from .models import Profile, College


class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    extra = 0

class ModifiedUserAdmin(UserenaAdmin):
    change_form_template = 'loginas/change_form.html'
    list_display = ('username', 'get_full_ar_name',
                    'get_full_en_name', 'get_college',
                    'get_student_id', 'email', 'get_mobile_number',
                    'is_active', 'date_joined')
    search_fields= ('username', 'email',
                    'profile__ar_first_name',
                    'profile__ar_middle_name',
                    'profile__ar_last_name',
                    'profile__en_first_name',
                    'profile__en_middle_name',
                    'profile__en_last_name',
                    'profile__student_id',
                    'profile__mobile_number')
    list_filter = ['profile__college', 'profile__city', 'profile__gender']

    inlines = [ProfileInline]

    def get_full_en_name(self, obj):
        try:
            return obj.profile.get_en_full_name()
        except ObjectDoesNotExist:
            return

    def get_full_ar_name(self, obj):
        try:
            return obj.profile.get_ar_full_name()
        except ObjectDoesNotExist:
            return

    def get_student_id(self, obj):
        try:
            return obj.profile.student_id
        except ObjectDoesNotExist:
            return

    def get_mobile_number(self, obj):
        try:
            return obj.profile.mobile_number
        except ObjectDoesNotExist:
            return

    def get_college(self, obj):
        try:
            return obj.profile.college
        except ObjectDoesNotExist:
            return

admin.site.unregister(User)
admin.site.register(User, ModifiedUserAdmin)
admin.site.register(College)
