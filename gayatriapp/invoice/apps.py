from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"


# class MyAdminConfig(AdminConfig):
#     default_site = "main.admin.MyAdminSite"
