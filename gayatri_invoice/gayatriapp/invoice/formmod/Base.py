from django.utils.html import format_html
from django.template import Template
from django.http import JsonResponse
from django import forms
from ..models import *
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
import json
import logging
logger = logging.getLogger(__name__)
# Simple base class - minimal change for immediate DRY benefits


class BaseInvoiceForm(forms.Form):
    """Base form class with common configuration"""
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    # Common choice options - eliminate duplication
    ORDER_TYPES = [
        ("local", "Local"),
        ("direct", "Direct"),
        ("export", "Export"),
    ]

    ORDER_TYPES_LOCAL_EXPORT = [
        ("local", "Local"),
        ("export", "Export"),
    ]

    YES_NO_CHOICES = [
        (True, "yes"),
        (False, "no")
    ]

    PLUS_MINUS_CHOICES = [
        (True, "plus"),
        (False, "minus")
    ]

# helper functions


def getInputFields(object):
    methods_list = [
        method
        for method in dir(object)
        if callable(getattr(object, method)) and not method.startswith("__")
    ]
    return methods_list


def button(name: str, hx_vals: dict, hx_req: str, target: str = "#dynform"):
    data = json.dumps(hx_vals)
    html = format_html('<input class="w3-button w3-ripple w3-green w3-padding w3-margin"\
                type="button" value="{}" \
                hx-post={} \
                hx-trigger="click" \
                hx-target={} \
                hx-swap="outerHTML" \
                hx-vals=\'{}\'/>', name, hx_req, target, data)
    return html

# auth forms


class loginForm(forms.Form):
    template_name = "login_snippet.html"
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


class changePassword(BaseInvoiceForm):

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


# admin forms
class adminCompany(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

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


class new_report(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    report_name = forms.SlugField()
    template_name = forms.SlugField()
    data_list = forms.JSONField()

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.fields['template_name'].choices = get_template_name()


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


class keyValueForm(forms.Form):
    key = forms.CharField()
    value = forms.CharField()


class reportEdit(forms.Form):
    template_name = "form_snippet.html"
    report_name = forms.ChoiceField(choices=[])


class reportDelete(forms.Form):
    template_name = "form_snippet.html"
    report_name = forms.ChoiceField(choices=[])


class table_list(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    company = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].choices = Company.objects.values_list(
            'id', 'company_name')


class table_create(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    table_name = forms.CharField(max_length=100)
    company = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].choices = Company.objects.values_list(
            'id', 'company_name')


class table_edit(forms.Form):
    template_name = "form_snippet.html"
    table_name = forms.ChoiceField(choices=[])


class table_delete(forms.Form):
    template_name = "form_snippet.html"
    table_name = forms.ChoiceField(choices=[])


class table_backup(forms.Form):
    template_name = "form_snippet.html"
    table_name = forms.ChoiceField(choices=[])
