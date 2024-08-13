from django.shortcuts import render, redirect
from django.utils.html import format_html
from django.http import JsonResponse,HttpResponse
from .formmod.Displayform import DisplayForm
from .formmod.CreateForm import formFieldData
from django.views.decorators.http import require_http_methods 
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .models import Profile, AdminProfile
from django.contrib.auth import authenticate
import json

# Create your views here.
class home():
    def index(request):
        return render(request,"main/index.html",{
                "nav":"navigation",
                "itemlist":DisplayForm.AddFields()
            })

    def start(request):
        return render(request,"main/home.html",{
                "home":DisplayForm.home(),
            })

class form():
    def create_form (request):
         # use the ui to get the no each type of field required in a queue 
         if request.method == "POST":
          data = request.POST.get("additem")
          return HttpResponse(DisplayForm.UserForm(data))
         else:
          return JsonResponse({"response":"other response"})
    
    def delete_form (request):
         if request.method == "POST":
          data = request.POST.get("something") 
          return JsonResponse({"response":"response"})
         else:
          return JsonResponse({"response":"other response"})
    
    def edit_form (request):
         if request.method == "POST":
          data = request.POST.get("something") 
          return JsonResponse({"response":"response"})
         else:
          return JsonResponse({"response":"other response"})

class report():
    
    def new_report (request):
         if request.method == "POST":
          data = request.POST.get("something") 
          return JsonResponse({"response":"response"})
         else:
          return JsonResponse({"response":"other response"})
    
    def edit_report (request):
         if request.method == "POST":
          data = request.POST.get("something") 
          return JsonResponse({"response":"response"})
         else:
          return JsonResponse({"response":"other response"})
    
    def delete_report (request):
         if request.method == "POST":
          data = request.POST.get("something") 
          return JsonResponse({"response":"response"})
         else:
          return JsonResponse({"response":"other response"})

class user():

    def login(request):
        if request.method == "POST":
            username = request.POST["Username"]
            password = request.POST["Password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return redirect("main:index")
            else:
                return render(request,"main/login.html",{"login":DisplayForm.loginFail()})
        else:
            return render(request,"main/login.html",{
                "login":DisplayForm.loginForm()
                }
            )
    def logout():
        pass
    
    def new_user (request):
     if request.method == "POST":
      data = request.POST.get("something") 
      return JsonResponse({"response":"response"})
     else:
      return JsonResponse({"response":"other response"})


    
    def edit_user (request):
     if request.method == "POST":
      data = request.POST.get("something") 
      return JsonResponse({"response":"response"})
     else:
      return JsonResponse({"response":"other response"})


    
    def delete_user (request):
     if request.method == "POST":
      data = request.POST.get("something") 
      return JsonResponse({"response":"response"})
     else:
      return JsonResponse({"response":"other response"})

class group():
    
    def new_group (request):
     if request.method == "POST":
      data = request.POST.get("something") 
      return JsonResponse({"response":"response"})
     else:
      return JsonResponse({"response":"other response"})
    
    def edit_group (request):
     if request.method == "POST":
      data = request.POST.get("something") 
      return JsonResponse({"response":"response"})
     else:
      return JsonResponse({"response":"other response"})
    
    def delete_group (request):
     if request.method == "POST":
      data = request.POST.get("something") 
      return JsonResponse({"response":"response"})
     else:
      return JsonResponse({"response":"other response"})

class db():
    
    def create_db (request):
     if request.method == "POST":
      data = request.POST.get("something") 
      return JsonResponse({"response":"response"})
     else:
      return JsonResponse({"response":"other response"})
    
    def createtable_db (request):
     if request.method == "POST":
      data = request.POST.get("something") 
      return JsonResponse({"response":"response"})
     else:
      return JsonResponse({"response":"other response"})
    
    def edittable_db (request):
     if request.method == "POST":
      data = request.POST.get("something") 
      return JsonResponse({"response":"response"})
     else:
      return JsonResponse({"response":"other response"})
    
    def deletetable_db (request):
     if request.method == "POST":
      data = request.POST.get("something") 
      return JsonResponse({"response":"response"})
     else:
      return JsonResponse({"response":"other response"})
    
    def backup (request):
     if request.method == "POST":
      data = request.POST.get("something") 
      return JsonResponse({"response":"response"})
     else:
      return JsonResponse({"response":"other response"})

