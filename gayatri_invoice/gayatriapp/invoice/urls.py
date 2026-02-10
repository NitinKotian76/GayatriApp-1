from django.urls import path
from . import views
from .all_views import admin_views, auth_views, common_views, form_views, report_views
from .all_views.millsoft import millsoft_master_view, millsoft_transaction_view, millsoft_report_view, millsoft_utility_view

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
millsoft_master_urlpatterns = [
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
    path("mcustomer/create/", millsoft_master_view.MCustomer_create.as_view(),
         name="MCustomer_create"),
    path("mcustomer/<int:pk>/update/", millsoft_master_view.MCustomer_update.as_view(),
         name="MCustomer_update"),
    path("mcustomer/<int:pk>/delete/", millsoft_master_view.MCustomer_delete.as_view(),
         name="MCustomer_delete"),
    path("mcustomer/", millsoft_master_view.MCustomer_list.as_view(),
         name="MCustomer_list"),
    path("mexportfields/create/", millsoft_master_view.MExportFields_create.as_view(),
         name="MExportFields_create"),
    path("mexportfields/<int:pk>/update/", millsoft_master_view.MExportFields_update.as_view(),
         name="MExportFields_update"),
    path("mexportfields/<int:pk>/delete/", millsoft_master_view.MExportFields_delete.as_view(),
         name="MExportFields_delete"),
    path("mexportfields/", millsoft_master_view.MExportFields_list.as_view(),
         name="MExportFields_list"),
    path("mitem/create/", millsoft_master_view.MItem_create.as_view(),
         name="MItem_create"),
    path("mitem/<int:pk>/update/", millsoft_master_view.MItem_update.as_view(),
         name="MItem_update"),
    path("mitem/<int:pk>/delete/", millsoft_master_view.MItem_delete.as_view(),
         name="MItem_delete"),
    path("mitem/", millsoft_master_view.MItem_list.as_view(),
         name="MItem_list"),
    path("mitemcategory/create/", millsoft_master_view.MItemCategory_create.as_view(),
         name="MItemCategory_create"),
    path("mitemcategory/<int:pk>/update/", millsoft_master_view.MItemCategory_update.as_view(),
         name="MItemCategory_update"),
    path("mitemcategory/<int:pk>/delete/",
         millsoft_master_view.MItemCategory_delete.as_view(), name="MItemCategory_delete"),
    path("mitemcategory/", millsoft_master_view.MItemCategory_list.as_view(),
         name="MItemCategory_list"),
    path("mlocation/create/", millsoft_master_view.MLocation_create.as_view(),
         name="MLocation_create"),
    path("mlocation/<int:pk>/update/",
         millsoft_master_view.MLocation_update.as_view(), name="MLocation_update"),
    path("mlocation/<int:pk>/delete/",
         millsoft_master_view.MLocation_delete.as_view(), name="MLocation_delete"),
    path("mlocation/", millsoft_master_view.MLocation_list.as_view(),
         name="MLocation_list"),
    path("mplusminushead/create/", millsoft_master_view.MPlusMinusHead_create.as_view(),
         name="MPlusMinusHead_create"),
    path("mplusminushead/<int:pk>/update/",
         millsoft_master_view.MPlusMinusHead_update.as_view(), name="MPlusMinusHead_update"),
    path("mplusminushead/<int:pk>/delete/", millsoft_master_view.MPlusMinusHead_delete.as_view(),
         name="MPlusMinusHead_delete"),
    path("mplusminushead/", millsoft_master_view.MPlusMinusHead_list.as_view(),
         name="MPlusMinusHead_list"),
    path("mshade/create/", millsoft_master_view.MShade_create.as_view(),
         name="MShade_create"),
    path("mshade/<int:pk>/update/", millsoft_master_view.MShade_update.as_view(),
         name="MShade_update"),
    path("mshade/<int:pk>/delete/", millsoft_master_view.MShade_delete.as_view(),
         name="MShade_delete"),
    path("mshade/", millsoft_master_view.MShade_list.as_view(),
         name="MShade_list"),
    path("msupplier/create/", millsoft_master_view.MSupplier_create.as_view(),
         name="MSupplier_create"),
    path("msupplier/<int:pk>/update/", millsoft_master_view.MSupplier_update.as_view(),
         name="MSupplier_update"),
    path("msupplier/<int:pk>/delete/", millsoft_master_view.MSupplier_delete.as_view(),
         name="MSupplier_delete"),
    path("msupplier/", millsoft_master_view.MSupplier_list.as_view(),
         name="MSupplier_list"),

]

millsoft_transact_urlpatterns = [
    path("tproduction/", millsoft_transaction_view.TProduction_list.as_view(),
         name="TProduction_list"),
    path("tproduction/create/", millsoft_transaction_view.TProduction_create.as_view(),
         name="TProduction_create"),
    path("tproduction/<int:pk>/delete/",
         millsoft_transaction_view.TProduction_delete.as_view(), name="TProduction_delete"),
    path("texportdetails/create/", millsoft_transaction_view.TExportDetails_create.as_view(),
         name="TExportDetails_create"),
    path("texportdetails/<int:pk>/update/", millsoft_transaction_view.TExportDetails_update.as_view(),
         name="TExportDetails_update"),
    path("texportdetails/<int:pk>/delete/", millsoft_transaction_view.TExportDetails_delete.as_view(),
         name="TExportDetails_delete"),
    path("texportdetails/", millsoft_transaction_view.TExportDetails_list.as_view(),
         name="TExportDetails_list"),
    path("tindent/create/", millsoft_transaction_view.TIndent_create.as_view(),
         name="TIndent_create"),
    path("tindent/<int:pk>/update/", millsoft_transaction_view.TIndent_update.as_view(),
         name="TIndent_update"),
    path("tindent/<int:pk>/delete/", millsoft_transaction_view.TIndent_delete.as_view(),
         name="TIndent_delete"),
    path("tindent/", millsoft_transaction_view.TIndent_list.as_view(),
         name="TIndent_list"),
    path("tinvoice/create/", millsoft_transaction_view.TInvoice_create.as_view(),
         name="TInvoice_create"),
    path("tinvoice/<int:pk>/update/", millsoft_transaction_view.TInvoice_update.as_view(),
         name="TInvoice_update"),
    path("tinvoice/<int:pk>/delete/", millsoft_transaction_view.TInvoice_delete.as_view(),
         name="TInvoice_delete"),
    path("tinvoice/", millsoft_transaction_view.TInvoice_list.as_view(),
         name="TInvoice_list"),

    path("tproduction/create/", millsoft_transaction_view.TProduction_create.as_view(),
         name="TProduction_create"),
    path("tproduction/<int:pk>/update/", millsoft_transaction_view.TProduction_update.as_view(),
         name="TProduction_update"),
    path("tproduction/<int:pk>/delete/", millsoft_transaction_view.TProduction_delete.as_view(),
         name="TProduction_delete"),
    path("tproduction/", millsoft_transaction_view.TProduction_list.as_view(),
         name="TProduction_list"),
    path("tproductionbck/create/", millsoft_transaction_view.TProduction_bck_create.as_view(),
         name="TProduction_bck_create"),
    path("tproductionbck/<int:pk>/update/", millsoft_transaction_view.TProduction_bck_update.as_view(),
         name="TProduction_bck_update"),
    path("tproductionbck/<int:pk>/delete/", millsoft_transaction_view.TProduction_bck_delete.as_view(),
         name="TProduction_bck_delete"),
    path("tproductionbck/", millsoft_transaction_view.TProduction_bck_list.as_view(),
         name="TProduction_bck_list"),
    path("tproductionreel/create/", millsoft_transaction_view.TProductionReel_create.as_view(),
         name="TProductionReel_create"),
    path("tproductionreel/<int:pk>/update/", millsoft_transaction_view.TProductionReel_update.as_view(),
         name="TProductionReel_update"),
    path("tproductionreel/<int:pk>/delete/", millsoft_transaction_view.TProductionReel_delete.as_view(),
         name="TProductionReel_delete"),
    path("tproductionreel/", millsoft_transaction_view.TProductionReel_list.as_view(),
         name="TProductionReel_list"),
]

millsoft_report_urlpatterns = [
    path("rchallan/create/", millsoft_report_view.RChallan_create,
         name="RChallan_create"),
    path("rchallan/download/<str:filename>/", millsoft_report_view.download_challan,
         name="download_challan"),

]
millsoft_utility_urlpatterns = [

    path("stocktransfer/", millsoft_utility_view.StockTransfer.as_view(),
         name="StockTransfer"),
]

millsoft_urlpatterns = (
    millsoft_master_urlpatterns +
    millsoft_transact_urlpatterns +
    millsoft_report_urlpatterns +
    millsoft_utility_urlpatterns
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
