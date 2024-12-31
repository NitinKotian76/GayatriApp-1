from django.urls import path
from .formmod import BaseForm
from . import views

app_name="main"

urlpatterns = [
    path('',views.login_user.as_view(),name="login"),
    path('index',views.index.as_view(), name="index"),
    path('profile_user',views.profile_user.as_view(), name="profile_user"),
	# path('new_user',views.user.new_user,name="new_user"),
	# path('edit_user',views.user.edit_user,name="edit_user"),
	# path('delete_user',views.user.delete_user,name="delete_user"),
	path('form_setup',views.form_setup.as_view(),name="form_setup"),
	# path('delete_form',views.form.delete_form,name="delete_form"),
	# path('edit_form',views.form.edit_form,name="edit_form"),
	path('field_setup',views.field_setup.as_view(),name="field_setup"),
	# path('rm_field',views.form.rm_field,name="rm_field"),
	# path('edit_field',views.form.edit_field,name="edit_field"),
	# path('save_field_config',views.form.save_field_config,name="save_field_config"),
	# path('new_report',views.report.new_report,name="new_report"),
	# path('edit_report',views.report.edit_report,name="edit_report"),
	# path('delete_report',views.report.delete_report,name="delete_report"),
	# path('new_group',views.group.new_group,name="new_group"),
	# path('edit_group',views.group.edit_group,name="edit_group"),
	# path('delete_group',views.group.delete_group,name="delete_group"),
	# path('create_db',views.db.create_db,name="create_db"),
	# path('createtable_db',views.db.createtable_db,name="createtable_db"),
	# path('edittable_db',views.db.edittable_db,name="edittable_db"),
	# path('deletetable_db',views.db.deletetable_db,name="deletetable_db"),
	# path('backup',views.db.backup,name="backup"),
	# path('cancel',views.form.cancel,name="cancel"),
]
