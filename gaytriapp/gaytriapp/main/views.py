from django.shortcuts import render
from django.utils.html import format_html
from django.template import Template

from . import BaseForm as BF


# Create your views here.
def index(request):
    return render(request,"main/Index.html",{"appname":"Gayatriapp"})

def sample(request):
    return render(request,"main/Samples.html",{"children":BF.form(BF.text_input()+BF.text_input()+BF.text_input2())})