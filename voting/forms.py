# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django import forms

from .models import Nomination

class NominationForm(forms.ModelForm):
    class Meta:
        model = Nomination
        fields = ['plan', 'cv', 'certificates']
