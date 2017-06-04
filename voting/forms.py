# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django import forms
from . import models
from dal import autocomplete

class NominationForm(forms.ModelForm):
    class Meta:
        model = models.Nomination
        fields = ['plan', 'cv', 'certificates', 'gpa']

# To be used in the admin interface, for autocompletion field.
class UnelectedWinnerForm(forms.ModelForm):
    class Meta:
        model = models.UnelectedWinner
        fields = ('__all__')
        widgets = {
            'user': autocomplete.ModelSelect2(url='voting:user-autocomplete', attrs={'data-html': 'true'})
        }
