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
    table_list = forms.ChoiceField(widget=forms.Select(
        choices=[], attrs={
            "id": "table_list"
        }))

    def __init__(self, *args, **kwargs):
        company = None
        if 'company' in kwargs:
            company = kwargs.pop('company')
        super().__init__(*args, **kwargs)
        self.fields['company'].choices = [(None, "--------")] + list(Company.objects.values_list(
            'id', 'company_name'))
        if self.data.get('company'):
            company = self.data.get('company')
        if not company:
            first_company = Company.objects.first()
            company = first_company.id if not first_company else None
        logger.debug(f"company id {company}")
        self.fields['table_list'].choices = [(None, "--------")] + list(
            TableName.objects.filter(company=company).values_list('id', 'table_name'))


class table_create(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    table_name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
    company = forms.ChoiceField(choices=[])

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
