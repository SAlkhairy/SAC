# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django import forms
from . import models

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = ['city', 'college', 'email', 'type',
                  'title', 'description', 'picture']

class DebateQForm(forms.ModelForm):
    class Meta:
        model = models.DebateQ
        fields = ['question']