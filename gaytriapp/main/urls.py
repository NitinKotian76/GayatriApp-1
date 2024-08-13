from django.urls import path
from .formmod import BaseForm
from . import views

app_name="main"

urlpatterns = [
    path('', views.home.start, name="start"),
    path('login',views.user.login,name="login"),
    path('index',views.home.index, name="index"),
	path('create_form',views.form.create_form,name="create_form"),
	path('delete_form',views.form.delete_form,name="delete_form"),
	path('edit_form',views.form.edit_form,name="edit_form"),
	path('new_report',views.report.new_report,name="new_report"),
	path('edit_report',views.report.edit_report,name="edit_report"),
	path('delete_report',views.report.delete_report,name="delete_report"),
	path('new_user',views.user.new_user,name="new_user"),
	path('edit_user',views.user.edit_user,name="edit_user"),
	path('delete_user',views.user.delete_user,name="delete_user"),
	path('new_group',views.group.new_group,name="new_group"),
	path('edit_group',views.group.edit_group,name="edit_group"),
	path('delete_group',views.group.delete_group,name="delete_group"),
	path('create_db',views.db.create_db,name="create_db"),
	path('createtable_db',views.db.createtable_db,name="createtable_db"),
	path('edittable_db',views.db.edittable_db,name="edittable_db"),
	path('deletetable_db',views.db.deletetable_db,name="deletetable_db"),
	path('backup',views.db.backup,name="backup"),

]
