from django import forms
from .models import SelectedSite
from dataplot.DataTools import AnalysisDriver

# class SiteSelector(forms.Form):
#     Site_Choice = forms.MultipleChoiceField(
#     required = True,
#     widget = forms.CheckboxSelectMultiple,
#     choices = SITE_CHOICES,
#     label = ' Choose sites:'
#     )

# Have only one site available at a time (for now)

class SiteSelector(forms.Form):
    ## The list of sites available
    SITE_CHOICES = [
        ('Heathfield', 'Heathfield'),
        ('Edinburgh', 'Edinburgh'),
        ]
    Site_Choice = forms.ChoiceField(
    required = True,
    # widget = forms.RadioSelect,
    choices = SITE_CHOICES,
    label = 'Choose a site'
    )

## Whether to combine sites or not

COMBINED_CHOICES = (
    ('combined', 'Combined'),
    ('seperate', 'Seperate'),
)

class VarCombine(forms.Form):
    Var_Combine = forms.ChoiceField(
    required = True,
    widget = forms.RadioSelect,
    choices = COMBINED_CHOICES,
    label = 'Combine variable choices?'
    )

class VariableChoices(forms.Form):
    ## Variable choices

    def __init__(self, request, sites, *args, **kwargs):
        super(VariableChoices, self).__init__(*args, **kwargs)
        # See what site is selected and then display variables
        available_variables = AnalysisDriver.GetSiteVariables(sites)

        VARIABLE_CHOICES = [(name,name) for name in available_variables]

        self.fields['Variable_choices'] = forms.MultipleChoiceField(
        required = True,
        widget = forms.CheckboxSelectMultiple,
        choices = VARIABLE_CHOICES,
        label = 'Choose variables to analyse'
        )
