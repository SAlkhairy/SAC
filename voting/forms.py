from django import forms
from django.forms import ModelForm

from models import Nomination

class NominationForm(forms.ModelForm):
    class Meta:
        model = Nomination
        fields = ['plan',
                  'cv',
                  ]
