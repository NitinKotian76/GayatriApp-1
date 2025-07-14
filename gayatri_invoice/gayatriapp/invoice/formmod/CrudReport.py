from django import forms
from ..models import *
import logging

logger = logging.getLogger(__name__)


# NOTE: priority 2
class new_report(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    report_name = forms.SlugField()
    template_name = forms.SlugField()
    data_list = forms.JSONField()

    # def __init__(self):
    #     super().__init__(*args, **kwargs)
    #     self.fields['template_name'].choices = get_template_name()


class reportCreate(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    report_name = forms.CharField()
    company = forms.ChoiceField(choices=[])
    excel_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faields['company'].choices = Company.objects.values_list(
            'id', 'company_name')


class keyValueForm(forms.Form):
    key = forms.CharField()
    value = forms.CharField()


class reportEdit(forms.Form):
    template_name = "form_snippet.html"
    report_name = forms.ChoiceField(choices=[])


class reportDelete(forms.Form):
    template_name = "form_snippet.html"
    report_name = forms.ChoiceField(choices=[])
