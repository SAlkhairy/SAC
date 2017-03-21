# -*- coding: utf-8  -*-

from django import forms

from accounts.models import Profile

from userena.forms import SignupForm, EditProfileForm

class CustomSignupForm(SignupForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        fields = ['ar_name',
                  'en_name',
                  'email',
                  'password',
                  'city',
                  'gender',
                  'mobile_number',
                  'student_id',
                  ]

    ar_name = forms.CharField(label=(u'الاسم بالعربي'),
                                 max_length=100,
                                 required=True)

    en_name = forms.CharField(label=(u'الاسم بالإنجليزي'),
                                max_length=100,
                                required=True)


    def save(self):
        """
        Override the save method to save the first and last name to the user
        field.

        """
        # First save the parent form and get the user.
        new_user = super(CustomSignupForm, self).save()

        # Get the profile, the `save` method above creates a profile for each
        # user because it calls the manager method `create_user`.
        # See: https://github.com/bread-and-pepper/django-userena/blob/master/userena/managers.py#L65
        user_profile = new_user.get_profile()

        user_profile.ar_name = self.cleaned_data['ar_name']
        user_profile.en_name = self.cleaned_data['en_name']
        user_profile.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user






class CustomEditProfileForm(EditProfileForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        fields = ['ar_name',
                  'en_name',
                  'city',
                  'gender',
                  'mobile_number',
                  ]
