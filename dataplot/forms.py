from django import forms
from .models import SelectedSite

SITE_CHOICES = (
    ('Heathfield', 'Heathfield'),
    ('Edinburgh', 'Edinburgh'),
    )

class SiteSelector(forms.Form):
    Site_Choice = forms.MultipleChoiceField(
    required = True,
    widget = forms.CheckboxSelectMultiple,
    choices = SITE_CHOICES,
    label = ' Choose sites:'
    )

COMBINED_CHOICES = (
    ('combined', 'Combined'),
    ('seperate', 'Seperate'),
)

class SiteCombine(forms.Form):
    Site_Combine = forms.ChoiceField(
    required = True,
    widget = forms.RadioSelect,
    choices = COMBINED_CHOICES,
    label = 'Combine site choices?'
    )
