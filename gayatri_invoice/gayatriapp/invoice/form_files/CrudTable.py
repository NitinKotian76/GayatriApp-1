
###############
# PHASE 2
###############
from django import forms
from ..dbmod.dbfunctions import TYPE_DATA
from ..models import *
import logging
logger = logging.getLogger(__name__)


class table_list(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    company = forms.ChoiceField(widget=forms.Select(choices=[], attrs={
        "hx-post": "/invoice/table_list",
        "hx-trigger": "change",
        "hx-target": "#table_list",
        "hx-select": "#table_list",
        "hx-swap": "outerHTML"
    }))
    table_name = forms.ChoiceField(widget=forms.Select(
        choices=[], attrs={
            "id": "table_list",
            "hx-get": "/invoice/table_data_view",
            "hx-trigger": "change delay:400ms",
            "hx-target": "#tableshow",
            "hx-swap": "innerHTML",
        }))

    def __init__(self, *args, **kwargs):
        company = None
        tablename = None
        if 'company' in kwargs:
            company = kwargs.pop('company')
        if 'tablename' in kwargs:
            tablename = kwargs.pop('tablename')

        super().__init__(*args, **kwargs)
        # get list of company name
        self.fields['company'].choices = [(None, "--------")] + list(Company.objects.values_list(
            'id', 'company_name'))
        # check if the request has the company variable
        if self.data.get('company'):
            company = self.data.get('company')
        # if company var is not available put the first company name  or none
        if not company:
            first_company = Company.objects.first()
            company = first_company.id if not first_company else None
        # get the list of tablenames for the particular company
        self.fields['table_name'].choices = [(None, "--------")] + list(
            TableName.objects.filter(company=company).values_list('table_name', 'table_name'))


class table_create(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    table_name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
    company = forms.ChoiceField(choices=[])
    duplicates_allowed = forms.BooleanField(
        widget=forms.NullBooleanSelect(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].choices = list(Company.objects.values_list(
            'id', 'company_name'))


class table_metadata(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    column = forms.CharField()
    data_type = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_type'].choices = TYPE_DATA


class table_edit(forms.Form):
    template_name = "form_snippet.html"
    table_name = forms.ChoiceField(choices=[])


class table_delete(forms.Form):
    template_name = "form_snippet.html"
    table_name = forms.ChoiceField(choices=[])


class table_backup(forms.Form):
    template_name = "form_snippet.html"
    table_name = forms.ChoiceField(choices=[])
