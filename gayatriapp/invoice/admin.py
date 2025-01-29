from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Form  # , Table
# Register your models here.

# @admin.action(description= "this is an action ")
# def someaction(ModelAdmin,request,queryset):
#     pass

@admin.register(UserProfile,UserAdmin)
class UserProfile(UserAdmin):
    list_display = ["userName", "userAccess", "userLog"]


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ["formName", "id", "formData"]


# @admin.register(Table)
# class TableAdmin(admin.ModelAdmin):
#     list_display = ["TableName","TableData","TablePermission"]


@admin.register(MyAdminSite, name="myadmin")
class MyAdminSite(admin.AdminSite):
    site_header = "Admin Page"
    site_title = "My Admin Portal"
    index_title = "Welcome to My Admin"
