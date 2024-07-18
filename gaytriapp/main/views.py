from django.shortcuts import render
from django.utils.html import format_html
from django.http import JsonResponse
from .formmod.Displayform import DisplayForm
from django.views.decorators.http import require_http_methods 
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .models import Profile, AdminProfile
import json

# Create your views here.
@ensure_csrf_cookie
def index(request):
 return render(request,"main/Index.html",{
   "nav":"navigation",
   "formDisplay":DisplayForm.loginForm()
  }
 )

@ensure_csrf_cookie
def login(request):
 csrf=request.META.get("CSRF_COOKIE")
 return render(request,"main/login.html",{
    "login":DisplayForm.loginForm(csrf=csrf)
   }
  )

@ensure_csrf_cookie
def create_form (request):
 if request.method == "POST":
  data = request.POST.get("something")
  return JsonResponse({"response":"response"})
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

