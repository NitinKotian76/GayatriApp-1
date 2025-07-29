from django import forms
from ..models import *
import logging

logger = logging.getLogger(__name__)


# NOTE: priority 2
class reportCreate(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    report_name = forms.CharField()
    company = forms.ChoiceField(choices=[])
    excel_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].choices = Company.objects.values_list(
            'id', 'company_name')

# sub-forms runtime additions


class keyValueForm(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    key = forms.CharField()
    value = forms.CharField()

# Filters
# add filters as per requirement


class datefilters(forms.Form):
    # add default filters
    from_date = forms.DateField()
    to_date = forms.DateField()


class reportEdit(forms.Form):
    template_name = "form_snippet.html"
    report_name = forms.ChoiceField(choices=[])


class reportDelete(forms.Form):
    template_name = "form_snippet.html"
    report_name = forms.ChoiceField(choices=[])
