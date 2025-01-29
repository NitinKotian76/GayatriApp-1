from django.urls import path
from .formmod import BaseForm
from . import views
from .admin import admin_site

app_name="invoice"

urlpatterns = [
    path('',views.login_user.as_view(), name="login"),
    path('index',views.index.as_view(), name="index"),
    path('profile_user',views.profile_user.as_view(), name="profile_user"),
	path('form_setup',views.form_setup.as_view(), name="form_setup"),
	path('field_setup',views.field_setup.as_view(), name="field_setup"),
]
