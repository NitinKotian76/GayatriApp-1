from django.urls import path

from . import views

app_name = "invoice"

urlpatterns = [
    path("", views.login_user.as_view(), name="login"),
    path("index", views.index, name="index"),
    path("profile_user", views.profile_user.as_view(), name="profile_user"),
    path("form_setup", views.form_setup.as_view(), name="form_setup"),
    path("form_delete", views.form_delete, name="form_delete"),
    path("form_config", views.form_config, name="form_config"),
    path("form_edit", views.form_edit, name="form_edit"),
    path("field_setup", views.field_setup.as_view(), name="field_setup"),
]
