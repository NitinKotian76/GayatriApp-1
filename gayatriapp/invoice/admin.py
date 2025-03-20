from .forms import *
from .models import CustomUser, Form, Table
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# Register your models here.

# Extending default User model


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    def group_name(self, obj):
        name = ""
        for group in obj.group.all():
            name += group.name + ","
        return name

    list_display = [
        "user_emp_code",
        "email",
        "user_name",
        "company",
        "is_admin",
        "is_staff",
        "is_active",
        "group_name",
    ]
    list_filter = ["user_name", "company"]

    fieldsets = [
        (
            None,
            {"fields": ["user_emp_code", "company", "email", "password", "group"]},
        ),
        ("Personal info", {"fields": ["user_name"]}),
        ("Permissions", {"fields": ["is_admin", "is_staff", "is_active"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "user_name",
                    "company",
                    "password1",
                    "password2",
                    "group",
                ],
            },
        ),
    ]
    search_fields = ["user_name", "user_emp_code"]
    ordering = ["user_name", "user_emp_code", "company"]
    filter_horizontal = []


admin.site.register(CustomUser, UserAdmin)
# admin.site.unregister(Group)


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    form = FormForm

    def group_name(self, obj):
        name = ""
        for group in obj.group.all():
            name += group.name + ","
        return name

    list_display = [
        "form_name",
        "group_name",
        "company",
    ]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):

    def group_name(self, obj):
        name = ""
        for group in obj.group.all():
            name += group.name + ","
        return name

    list_display = [
        "report_name",
        "group_name",
        "company",
    ]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["company_name"]


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["table_name"]
