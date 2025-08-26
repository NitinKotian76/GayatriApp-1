from django.urls import path, include
from . import views
from .all_views import *

app_name = "invoice"
# names with sentencecase are class based views
# Report URLs
report_urlpatterns = [
    path("report_view", report_views.report_view, name="report_view"),
    path("report_list", report_views.report_list, name="report_list"),
    path("new_report", report_views.new_report, name="new_report"),
    path("add_formset_field", report_views.add_formset_field,
         name="add_formset_field"),
]

# Form URLs
form_urlpatterns = [
    path("form_view", form_views.form_view, name="form_view"),
    path("select_row", form_views.select_row, name="select_row"),
    path("reset_selected_row", form_views.reset_selected_row,
         name="reset_selected_row"),
    path("delete_row", form_views.delete_row, name="delete_row"),
    path("approve_row", form_views.approve_row, name="approve_row"),
    path("form_list", form_views.form_list, name="form_list"),
    path("form_setup", form_views.form_setup, name="form_setup"),
    path("form_delete", form_views.form_delete, name="form_delete"),
    path("form_config", form_views.form_config, name="form_config"),
    path("form_edit", form_views.form_edit, name="form_edit"),
    path("field_setup", form_views.field_setup, name="field_setup"),
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
    path("table_list", admin_views.table_list, name="table_list"),
    path("create_table", admin_views.create_table, name="create_table"),
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
