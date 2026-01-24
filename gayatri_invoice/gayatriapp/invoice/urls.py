from django.urls import path, include
from . import views
from .all_views import admin_views, auth_views, common_views, form_views, report_views
from .all_views.millsoft import millsoft_master_view, millsoft_transaction_view, millsoft_report_view

app_name = "invoice"
# names with sentencecase are class based views
# Report URLs
report_urlpatterns = [
    path("report_view", report_views.report_view, name="report_view"),
    path("report_list", report_views.report_list, name="report_list"),
    path("new_report", report_views.new_report, name="new_report"),
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
    path("table_view_search", form_views.table_view_search,
         name="table_view_search"),
]

# Main URLs
main_urlpatterns = [
    path("index", common_views.index, name="index"),
    path("profile_user", common_views.profile_user, name="profile_user"),
    path("get_notifications", common_views.get_notifications.as_view(),
         name="get_notifications"),
    path("add_formset_field/<str:formname>", common_views.add_formset_field,
         name="add_formset_field"),
]

# Admin URLs
admin_urlpatterns = [
    path("table_list", admin_views.table_list, name="table_list"),
    path("create_table", admin_views.create_table, name="create_table"),
    path("admin_company", admin_views.admin_company, name="admin_company"),
]
# millsoft static
millsoft_master_urls = [
    path("magent/create/", millsoft_master_view.MAgent_create.as_view(),
         name="MAgent_create"),
    path("magent/<int:pk>/update/", millsoft_master_view.MAgent_update.as_view(),
         name="MAgent_update"),
    path("magent/<int:pk>/delete/", millsoft_master_view.MAgent_delete.as_view(),
         name="MAgent_delete"),
    path("magent/", millsoft_master_view.MAgent_list.as_view(), name="MAgent_list"),

    path("mcategory/create/", millsoft_master_view.MCategory_create.as_view(),
         name="MCategory_create"),
    path("mcategory/<uuid:pk>/update/",
         millsoft_master_view.MCategory_update.as_view(), name="MCategory_update"),
    path("mcategory/<uuid:pk>/delete/",
         millsoft_master_view.MCategory_delete.as_view(), name="MCategory_delete"),
    path("mcategory/", millsoft_master_view.MCategory_list.as_view(),
         name="MCategory_list"),

]
millsoft_transact_urls = [
    path("tproduction/", millsoft_transaction_view.TProduction_list.as_view(),
         name="TProduction_list"),
    path("tproduction/create/", millsoft_transaction_view.TProduction_create.as_view(),
         name="TProduction_create"),
    path("tinvoice/create/", millsoft_transaction_view.TInvoice_create.as_view(),
         name="TInvoice_create"),
    path("tinvoice/<int:pk>/update/", millsoft_transaction_view.TInvoice_update.as_view(),
         name="TInvoice_update"),
    path("tinvoice/<int:pk>/delete/", millsoft_transaction_view.TInvoice_delete.as_view(),
         name="TInvoice_delete"),
    path("tinvoice/", millsoft_transaction_view.TInvoice_list.as_view(),
         name="TInvoice_list"),
]
millsoft_report_urls = [
    path("rchallan/create/", millsoft_report_view.RChallan_create,
         name="RChallan_create"),
    path("rchallan/download/<str:filename>/", millsoft_report_view.download_challan,
         name="download_challan"),

]

millsoft_urlpatterns = (
    millsoft_master_urls +
    millsoft_transact_urls +
    millsoft_report_urls
)
# Combine all URL patterns
urlpatterns = (
    auth_urlpatterns +
    form_urlpatterns +
    table_urlpatterns +
    report_urlpatterns +
    admin_urlpatterns +
    main_urlpatterns +
    millsoft_urlpatterns
)
