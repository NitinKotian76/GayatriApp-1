from django.shortcuts import render
from django.utils.html import format_html
from django.template import Template
from django.http import JsonResponse
from .formmod.crudmod.Displayform import DisplayForm
from django.views.decorators.http import require_http_methods
import json

# Create your views here.
def index(request):
    return render(request,"main/Index.html",{"appname":"Gayatriapp"})


@require_http_methods(['GET'])
def sample(request):
    data = {"message":"Hello"}
    return JsonResponse(data)
    
    
    
    
    
    
    
    # if request.method == "GET": 
    #     data = json.loads(request.body)
    #     form = DisplayForm.htmlForm(request.method.GET.get("type"))
    #     return render(request,"main/Samples.html",{"form":form})
    # else:
    #     return render(request,"main/Samples.html",{"children":DisplayForm.show()})