from django.urls import path
from .formmod.crudmod import BaseForm
from . import views


app_name="main"
urlpatterns = [
    path('',views.index, name="index"),
    path('samples/',views.sample, name="samples")
]
