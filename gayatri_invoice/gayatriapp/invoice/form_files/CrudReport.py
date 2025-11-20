from django import forms
from ..models import *
import logging

logger = logging.getLogger(__name__)


class formClass(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class reportCreate(formClass):

    template_name = forms.CharField()
    sheet_name = forms.CharField()
    company = forms.ChoiceField(choices=[])
    excel_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].choices = Company.objects.values_list(
            'id', 'company_name')

# sub-forms runtime additions


class reportKeyValueForm(formClass):

    template_name = None
    key = forms.CharField()
    value = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].choices = Company.objects.values_list(
            'id', 'company_name')


# Filters
# add filters as per requirement


class datefilters(formClass):
    # add default filters
    template_name = None
    from_date = forms.DateField()
    to_date = forms.DateField()


class reportEdit(formClass):
    template_name = None
    report_name = forms.ChoiceField(choices=[])


class reportDelete(formClass):
    report_name = forms.ChoiceField(choices=[])
