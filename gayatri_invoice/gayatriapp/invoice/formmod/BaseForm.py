from django.utils.html import format_html
from django.template import Template
from django.http import JsonResponse
from django import forms
from ..models import *
from . import formComponents
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


def getInputFields(object):
    methods_list = [
        method
        for method in dir(object)
        if callable(getattr(object, method)) and not method.startswith("__")
    ]
    return methods_list


class base:
    global ButtonStyle, InputStyle, RowCellStyle, RowStyle, leftSpace, globalSpacing, TextAlignCenter, cellSpacing
    ButtonStyle = " w3-cell w3-button w3-blue w3-round-large w3-ripple"
    globalSpacing = " w3-margin"
    cellSpacing = " w3-padding"
    leftSpace = " w3-margin-left"
    TextAlignCenter = " w3-center"
    InputStyle = " w3-card"


class loginForm(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    employee_id = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    # TODO: this statement interferes with migrations
    company_name = forms.ChoiceField(
        widget=forms.Select,
        choices=Company.objects.values_list("id", "company_name"),
        required=True
    )

    def user(self):
        return self.user

    def clean(self):
        logger.debug("cleaning data")
        cleaned_data = super().clean()
        empid = cleaned_data.get("employee_id")
        password = cleaned_data.get("password")
        compname = self.cleaned_data.get("company_name")
        user = authenticate(
            user_emp_code=empid,
            password=password,
        )
        logger.debug("%s, %s, %s", type(empid), password, user.__str__())
        if user is not None:
            self.user = user
            # same user can have accounts in different companies
            if user.company_id != int(compname):
                raise ValidationError("User is not from this company")
        else:
            raise ValidationError("Employee ID or Password is wrong")
        return cleaned_data


class formCreate(forms.Form):
    # Group.objects.all(), Table.objects.all()
    template_name = "form_snippet.html"
    form_name = forms.CharField()
    # TODO: this statement interferes with migrations
    group_names = forms.MultipleChoiceField(
        widget=forms.SelectMultiple, choices=Group.objects.values_list()
    )
    table_names = forms.MultipleChoiceField(
        widget=forms.SelectMultiple, choices=TableName.objects.all()
    )
    description = forms.CharField()


class fieldAdd(forms.Form):
    template_name = "form_snippet.html"
    field_name = forms.ChoiceField(
        widget=forms.Select, choices=getInputFields(formComponents)
    )
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


class reportView(forms.Form):
    pass


class reportCreate(forms.Form):
    excel_file = forms.FileField()
    single_entry = forms.CharField()
    subgroup_entry = forms.ChoiceField()


class var_columnEntry(forms.Form):
    var = forms.CharField()
    column = forms.CharField()


class reportEdit(forms.Form):
    pass


class reportDelete(forms.Form):
    pass


class table_view(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    table_list = forms.ChoiceField()


class table_create(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    table_name = forms.CharField(max_length=100)
    # NOTE: add this when dynamic form is done
    # form_name = forms.CharField(max_length=100)
    company = forms.ChoiceField(choices=Company.objects.all())


class table_edit(forms.Form):
    pass


class table_delete(forms.Form):
    pass


class table_backup(forms.Form):
    pass
