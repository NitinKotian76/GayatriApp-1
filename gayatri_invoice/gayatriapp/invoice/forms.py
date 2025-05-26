from django import forms
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )
    user_name = forms.CharField(label="User Name", widget=forms.TextInput)
    company = forms.ModelChoiceField(
        Company.objects.all(), to_field_name="company_name"
    )
    group = forms.ModelMultipleChoiceField(Group.objects.all())

    class Meta:
        model = CustomUser
        fields = ["email", "user_emp_code", "company", "user_name", "group"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()
    group = forms.ModelMultipleChoiceField(Group.objects.all())
    company = forms.ModelChoiceField(
        Company.objects.all(), to_field_name="company_name"
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "user_emp_code",
            "user_name",
            "company",
            "group",
            "is_active",
            "is_admin",
        ]


class FormForm(forms.ModelForm):
    group = forms.ModelMultipleChoiceField(Group.objects.all())

    class Meta:
        model = Form
        list_display = ["form_name", "group", "form_data"]
        fields = ("form_name", "group", "form_data")


class loginForm(forms.ModelForm):
    emp_id = forms.CharField()
    password = forms.CharField()
    company = forms.ModelChoiceField(
        Company.objects.all(), to_field_name="company_name")
