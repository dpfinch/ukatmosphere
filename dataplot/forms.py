from django import forms
from .models import SelectedSite

SITE_CHOICES = (
    ('Heathfield', 'Heathfield'),
    ('Edinburgh', 'Edinburgh'),
    )

class SiteSelector(forms.Form):
    Site_Choice = forms.ChoiceField(
    required = True,
    widget = forms.RadioSelect,
    choices = SITE_CHOICES,
    )
