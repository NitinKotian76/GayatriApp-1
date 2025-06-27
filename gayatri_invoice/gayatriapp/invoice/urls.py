from django.urls import path, include
from . import views
from .all_views import *

app_name = "invoice"

# Report URLs
report_urlpatterns = [
    path("report_view", report_views.report_view, name="report_view"),
]

# Form URLs
form_urlpatterns = [
    path("form_view", form_views.form_view, name="form_view"),
    path('select_row', form_views.select_row, name='select_row'),
]

# Authentication URLs
auth_urlpatterns = [
    path("", auth_views.login_user, name="login"),
    path("logout_user", auth_views.logout_user, name="logout_user"),
    path("change_password", auth_views.change_password, name="change_password"),
]

# Table URLs
table_urlpatterns = [
    path("table_data_view", form_views.table_data_view, name="table_data_view"),
]

# Main URLs
main_urlpatterns = [
    path("index", views.index, name="index"),
    path("profile_user", views.profile_user, name="profile_user"),
    path("get_notifications", views.get_notifications, name="get_notifications"),
]

# Admin URLs
admin_urlpatterns = [
    path("form_list", admin_views.form_list, name="form_list"),
    path("form_setup", admin_views.form_setup, name="form_setup"),
    path("form_delete", admin_views.form_delete, name="form_delete"),
    path("form_config", admin_views.form_config, name="form_config"),
    path("form_edit", admin_views.form_edit, name="form_edit"),
    path("field_setup", admin_views.field_setup, name="field_setup"),
    path("table_list", admin_views.table_list, name="table_list"),
    path("create_table", admin_views.create_table, name="create_table"),
    path("report_list", admin_views.report_list, name="report_list"),
    path("new_report", admin_views.new_report, name="new_report"),
    path("admin_company", admin_views.admin_company, name="admin_company"),
]

# Combine all URL patterns
urlpatterns = (
    auth_urlpatterns +
    form_urlpatterns +
    table_urlpatterns +
    report_urlpatterns +
    admin_urlpatterns +
    main_urlpatterns
)
