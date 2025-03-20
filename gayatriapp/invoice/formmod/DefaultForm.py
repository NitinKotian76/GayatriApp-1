from . import BaseForm as bf
from django import forms
import logging
from ..models import *

logger = logging.getLogger(__name__)


class loginForm(forms.Form):
    template_name = "form_snippet.html"
    empid = forms.IntegerField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    cmpname = forms.ChoiceField(
        widget=forms.Select, choices=Company.objects.values_list(), required=True
    )


class formCreate(forms.Form):
    # Group.objects.all(), Table.objects.all()
    template_name = "form_snippet.html"
    form_name = forms.CharField()
    group_names = forms.MultipleChoiceField(
        widget=forms.SelectMultiple, choices=Group.objects.values_list()
    )
    # table_names = forms.MultipleChoiceField(
    #     widget=forms.SelectMultiple, choices=Table.objects.all()
    # )
    description = forms.CharField()


class fieldAdd(forms.Form):
    template_name = "form_snippet.html"
    field_name = forms.ChoiceField(widget=forms.Select, choices=bf.getInputFields())
    var_name = forms.CharField()
    disabled = forms.ChoiceField(widget=forms.CheckboxInput)
    table_row = forms.IntegerField()
    table_column = forms.IntegerField()

    # attr = 'hx-post="/invoice/field_setup" hx-target="#mainform" hx-swap="none"',
    # attr = 'onclick=document.getElementById("modalView").style.display="none"',


class formDelete(forms.Form):
    # search field
    template_name = "form_snippet.html"
    form_name = forms.ChoiceField(widget=forms.Select, choices="")
    group_name = forms.ChoiceField()


class formEdit(forms.Form):
    form_name = forms.ChoiceField(widget=forms.Select, choices="")
    group_name = forms.ChoiceField()
    # attr=f'hx-get="/invoice/form_setup" hx-vals={jsonvalue} hx-target="none" hx-swap="none"',
    # attr='onclick=document.getElementById("modalView").style.display="none"',


class reportCreate(forms.Form):
    pass


class reportEdit(forms.Form):
    pass


class reportDelete(forms.Form):
    pass


class tableCreate(forms.Form):
    pass


class tableEdit(forms.Form):
    pass


class tableDelete(forms.Form):
    pass


class tableBackup(forms.Form):
    pass
