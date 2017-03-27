# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from accounts.models import Profile
from userena.forms import SignupForm, EditProfileForm
from userena.models import UserenaBaseProfile
from .models import College, gender_choices, college_choices, city_choices


class CustomSignupForm(SignupForm):
    ar_first_name = forms.CharField(label=Profile._meta.get_field('ar_first_name').verbose_name,
                                max_length=30)
    ar_middle_name = forms.CharField(label=Profile._meta.get_field('ar_middle_name').verbose_name,
                                max_length=30)
    ar_last_name = forms.CharField(label=Profile._meta.get_field('ar_last_name').verbose_name,
                                max_length=30)
    en_first_name = forms.CharField(label=Profile._meta.get_field('en_first_name').verbose_name,
                                max_length=30)
    en_middle_name = forms.CharField(label=Profile._meta.get_field('en_middle_name').verbose_name,
                                max_length=30)
    en_last_name = forms.CharField(label=Profile._meta.get_field('en_last_name').verbose_name,
                                max_length=30)
    en_last_name = forms.CharField(label=Profile._meta.get_field('en_last_name').verbose_name,
                                max_length=30)
    username = None
    mobile_number = forms.CharField(label=Profile._meta.get_field('mobile_number').verbose_name)
    student_id = forms.IntegerField(label=Profile._meta.get_field('student_id').verbose_name)

    gender = forms.CharField(label=u"الجندر", max_length=1, widget=forms.Select(choices=gender_choices))

    college = forms.CharField(label=u"الكلية", max_length=1, widget=forms.Select(choices=college_choices))

    city = forms.CharField(label=u"المدينة", max_length=1, widget=forms.Select(choices=city_choices))

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = u'البريد الإلكتروني الجامعي'
        self.fields['password1'].label = 'إنشاء كلمة سر'
        self.fields['password2'].label = 'تأكيد كلمة السر'

    def clean(self, *args, **kwargs):
        cleaned_data = super(CustomSignupForm, self).clean(*args, **kwargs)
        if 'email' in cleaned_data:
            cleaned_data['email'] = cleaned_data['email'].lower()
            if not cleaned_data['email'].endswith('ksau-hs.edu.sa'):
                email_msg = u"الرجاء إدخال بريد جامعي"
                self._errors['email'] = self.error_class([email_msg])
                del self.cleaned_data['email']

        if 'gender' in cleaned_data and \
           'city' in cleaned_data and \
           'college' in cleaned_data:
            # Make sure that the college choice is valid.
            try:
                self.college = College.objects.get(
                    name=cleaned_data['college'],
                    city=cleaned_data['city'],
                    gender=cleaned_data['gender'])
            except College.DoesNotExist:
                college_msg = u"ليست كلية مسجلة."
                # Add an error message to specific fields.
                self._errors['college'] = self.error_class([college_msg])
                self._errors['city'] = self.error_class([college_msg])
                self._errors['gender'] = self.error_class([college_msg])
                # Remove invalid fields
                del cleaned_data['college']
                del cleaned_data['city']
                del cleaned_data['gender']
        return cleaned_data

    def save(self):
        """
        Override the save method to save the new fields

        """
        # Derive usernames from email address
        self.cleaned_data['username'] = self.cleaned_data['email'].split('@')[0]
        # First save the parent form and get the user.
        new_user = super(CustomSignupForm, self).save()

        # Get the profile, the `save` method above creates a profile for each
        # user because it calls the manager method `create_user`.
        # See: https://github.com/bread-and-pepper/django-userena/blob/master/userena/managers.py#L65
        user_profile = new_user.profile

        user_profile.ar_first_name = self.cleaned_data['ar_first_name']
        user_profile.ar_middle_name = self.cleaned_data['ar_middle_name']
        user_profile.ar_last_name = self.cleaned_data['ar_last_name']
        user_profile.en_first_name = self.cleaned_data['en_first_name']
        user_profile.en_middle_name = self.cleaned_data['en_middle_name']
        user_profile.en_last_name = self.cleaned_data['en_last_name']
        user_profile.student_id = self.cleaned_data['student_id']
        print self.cleaned_data['student_id']
        user_profile.mobile_number = self.cleaned_data['mobile_number']
        user_profile.gender = self.cleaned_data['gender']
        user_profile.city = self.cleaned_data['city']
        user_profile.college = self.college

        user_profile.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user

class CustomEditProfileForm(EditProfileForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        fields = ['ar_first_name', 'ar_middle_name', 'ar_last_name',
                  'en_first_name', 'en_middle_name', 'en_last_name',
                  'city', 'gender', 'mobile_number', ]

class ModifiedAuthenticationForm(forms.Form):
    identification = forms.CharField(label=u"البريد",
                                        widget=forms.TextInput(attrs={'class': 'required'}),
                                        max_length=75,
                                        error_messages={'required': u"رجاءً أدخل بريدك الجامعي."})
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(attrs={'class': 'required'}, render_value=False))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(),
                                     required=False,
                                     label=u'تذكرني (مدّة شهر)')


    def clean(self):
        """
        Checks for the identification and password.

        If the combination can't be found will raise an invalid sign in error.

        """
        identification = self.cleaned_data.get('identification')
        password = self.cleaned_data.get('password')

        if identification and password:
            username = identification.split('@')[0]
            username = username.lower().strip()

            # The final username should be returned to userena to
            # process.
            self.cleaned_data['identification'] = username

            user = authenticate(username=username, password=password)

            if user is None:
                if not identification.endswith('ksau-hs.edu.sa'):
                    email_msg = u"الرجاء إدخال بريد جامعي"
                    self._errors['identification'] = self.error_class([email_msg])
                    del self.cleaned_data['identification']
                else:
                    raise forms.ValidationError("ليست البيانات صحيحة!")
            return self.cleaned_data
