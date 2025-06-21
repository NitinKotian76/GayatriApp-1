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

    employee_id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Employee ID'
            }),
        label="Employee ID",
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }),
        label="Password",
        required=True)

    company_name = forms.ModelChoiceField(
        queryset=Company.objects.none(),
        empty_label="Select Company",
        widget=forms.Select(attrs={}),
        to_field_name="id",
        label="company_name",
        required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].queryset = Company.objects.all()

    def clean(self):
        logger.debug("cleaning data")
        cleaned_data = super().clean()
        empid = cleaned_data.get("employee_id")
        password = cleaned_data.get("password")
        company = cleaned_data.get("company_name")

        try:
            user = authenticate(
                user_emp_code=empid,
                password=password,
            )
            if user is None:
                raise ValidationError("Employee ID or Password is wrong")
            if user.company_id != company.id:
                raise ValidationError("User is not from this company")
            self.user = user
            return cleaned_data
        except Exception as e:
            logger.error(e)
            raise ValidationError("An error occurred while logging in")


class changePassword(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Old Password'
        }),
        label="Old Password",
        required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'New Password'
        }),
        label="New Password",
        required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm Password'
        }),
        label="Confirm Password",
        required=True)


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
