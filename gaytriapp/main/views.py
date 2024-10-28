from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse 
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .models import Profile, AdminProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
import json

from .formmod.Displayform import DisplayForm as ds
from .formmod  import DefaultForm as df
from .formmod.CreateForm import formFieldData
from .formmod.LoadForm import Filedata

# Create your views here.
global  ff
# ds = DisplayForm()
ff = None
        

class home():
    def start(request):
        return render(request,"main/home.html",{
                "home":df.home()
            })

    def login(request):
        if request.method == "POST":
            username = request.POST["Username"]
            password = request.POST["Password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return redirect("main:index")
            else:
                return render(request,"main/login.html",{"login":df.loginFail()})
        else:
            return render(request,"main/login.html",{
                "login":df.loginForm()
                }
            )

    def index(request):
        request.session.setdefault('count',0) 
        return render(request,"main/index.html",{"itemlist":df.addFields()})
class user():

    def logout(self):
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

@login_required
class form():

    def create_form(request):
        """
        this view should get the user input and show the field config modal 
        then after the user clicks save or cancel the mainform should be updated
        """
        # initialize the form data
        if request.method == "GET":
            return HttpResponse(df.formSetup())

    def form_setup(request):
        # name the form , give permissions , attach tables to the form
        if request.method == "POST":
            if request.POST.get("submit"):
                formName = request.POST.get("formname")
                permissions = request.POST.get("permission")
                tables = request.POST.get("tables")
                # create formfield object
                ff=formFieldData(formname,permissions,tables)
                return HttpResponse("success")

    def save_form(request):
        if request.method == "POST":
            ff.saveForm(ff.FieldDataDict)
            return("success")
    
    def delete_form (request):
         if request.method == "POST":
             return(ff.deleteForm(ff.filename))
    
    def edit_form(request):
         if request.method == "POST":
             return render(request,"main/formEditor.html",{"itemlist":df.addFields()})

    def add_field(request):
        if request.method == "POST":
             data = request.POST.get("additem")
             # arguments = somefunction()
             if request.POST.get("additem") != None:# choose field
                 request.session['count'] = request.session.get('count',0)+1
                 print(request.session.get('count',0))
                 editable = True
                 # ff.addField(container,'')
                 label="hello"
                 attr="hide"
                 ff.addField(data,label,attr,"form1",request.session.get('count',0),child="no children")
                 return HttpResponse(Filedata(ff.filename))

    def edit_field(request):                
        return HttpResponse(df.fieldSetup())
    
    def save_field_config(request):
        if request.method == "POST":
            if request.POST.get("submit"):
                fieldName = request.POST.get("fieldname")
                permissions = request.POST.get("permission")
                tables = request.POST.get("tables")
                ff = formFieldData(formname,permissions,tables)
    def rm_field(request):
         fieldno=request.POST.get("rm_field")
         ff.removeField(fieldno)
         request.session['count'] = request.session.get('count',0)-1
         print(request.session.get('count',0))
         return HttpResponse(Filedata(ff.filename))


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

