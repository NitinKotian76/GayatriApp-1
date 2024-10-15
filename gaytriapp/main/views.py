from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse 
from .formmod.Displayform import DisplayForm,displayDefaultForms
from .formmod.CreateForm import formFieldData
from .formmod.LoadForm import Filedata
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .models import Profile, AdminProfile
from django.contrib.auth import authenticate
import json

# Create your views here.
global df,ds
df = displayDefaultForms()
ds = DisplayForm()

class home():
    def index(request):
        request.session.setdefault('count',0)
        return render(request,"main/index.html",{
                "nav":"navigation",
                "itemlist":df.addFields(),
            })

    def start(request):
        return render(request,"main/home.html",{
                "home":df.home()
            })

class form():
    @login_required
    def create_form (request):
        """
        this view should get the user input and show the field config modal 
        then after the user clicks save or cancel the mainform should be updated
        """
        # use the ui to get the no each type of field required in a queue 
        ff = formFieldData("demo1",[["user1","r","w","x"]],["table1","table2"])
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
        return HttpResponse(df.fieldConfig())
    
    def save_config(request):
        pass
    def rm_field(request):
         fieldno=request.POST.get("rm_field")
         ff.removeField(fieldno)
         request.session['count'] = request.session.get('count',0)-1
         print(request.session.get('count',0))
         return HttpResponse(Filedata(ff.filename))

    def save_form(request):
        pass
    
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
                return render(request,"main/login.html",{"login":df.loginFail()})
        else:
            return render(request,"main/login.html",{
                "login":df.loginForm()
                }
            )
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

