from django.urls import path
from .formmod import BaseForm
from . import views

app_name="main"

urlpatterns = [
    path('',views.login, name="login"),
    path('index',views.index, name="index"),
	path('create_form',views.create_form,name="create_form"),
	path('delete_form',views.delete_form,name="delete_form"),
	path('edit_form',views.edit_form,name="edit_form"),
	path('new_report',views.new_report,name="new_report"),
	path('edit_report',views.edit_report,name="edit_report"),
	path('delete_report',views.delete_report,name="delete_report"),
	path('new_user',views.new_user,name="new_user"),
	path('edit_user',views.edit_user,name="edit_user"),
	path('delete_user',views.delete_user,name="delete_user"),
	path('new_group',views.new_group,name="new_group"),
	path('edit_group',views.edit_group,name="edit_group"),
	path('delete_group',views.delete_group,name="delete_group"),
	path('create_db',views.create_db,name="create_db"),
	path('createtable_db',views.createtable_db,name="createtable_db"),
	path('edittable_db',views.edittable_db,name="edittable_db"),
	path('deletetable_db',views.deletetable_db,name="deletetable_db"),
	path('backup',views.backup,name="backup"),

]
