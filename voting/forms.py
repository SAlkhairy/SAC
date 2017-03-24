# -*- coding: utf-8  -*-
from __future__ import unicode_literals


from django import forms
from django.forms import ModelForm

from models import Nomination, Position

class PositionForm(forms.ModelForm):
    gender_choices = (
    ('F', 'طالبة'),
    ('M', 'طالب'),
    )
    gender = forms.ChoiceField(choices=gender_choices)



