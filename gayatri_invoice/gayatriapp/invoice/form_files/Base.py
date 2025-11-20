from django import forms
from ..models import *
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
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
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['company_name'].queryset = Company.objects.all()

    def clean(self):
        logger.debug("cleaning data")
        cleaned_data = super().clean()
        empid = cleaned_data.get("employee_id")
        password = cleaned_data.get("password")
        company = cleaned_data.get("company_name")
        request = self.request

        try:
            user = authenticate(
                request=request,
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
