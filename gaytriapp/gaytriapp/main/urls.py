from django.urls import path
from . import views,BaseForm


app_name="main"
urlpatterns = [
    path('',views.index, name="Index"),
    path('samples/',views.sample, name="Samples")
]
