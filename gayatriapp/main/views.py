from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse 
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .models import UserProfile, Forms
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate
import json
from django.core.cache import cache

from .formmod.Displayform import DisplayForm as ds
from .formmod  import DefaultForm as df
from .formmod.CreateForm import formFieldData
from .formmod.LoadForm import Filedata

# Create your views here.
global  count_set
# ds = DisplayForm()
count_set = 0
        
# anything that is returned by the rendered template should be validated by the client and then the server
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
        return render(request,"main/index.html",{"itemlist":df.addFields()})

class user():

    def logout(self):
        pass
    
    def new_user (request):
        pass

    def edit_user (request):
        pass

    def delete_user (request):
        pass

@login_required
class form():

    def create_form(request):
        """
        this def displays an form info editor
        """
        # initialize the form data
        if request.method == "GET":
            return HttpResponse(df.formConfig())

    def form_setup(request):
        # name the form , give permissions , attach tables to the form
        """
        this def gets the input from the form info page and sets up the form data in json
        """
        if request.method == "POST":
            formName = request.POST.get("Form Name")
            userName = request.POST.get("User Name")
            read= request.POST.get("Read")
            write= request.POST.get("Write")
            TableNames = request.POST.get("Tables")
            ## can add edit acceess
            description= request.POST.get("Description")
            Access_rights = {userName:[read,write]} ## username as key to the access rights 
            tables = {"tables":TableNames}
            ff=formFieldData(formName,Access_rights,tables) #### this variable is present in the class
            response = redirect("/main/edit_field") ## this i am doing to display success from the server
            return response

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
             if request.POST.get("additem") != None:# choose field
                label = request.POST.get(label)

                tableRow = request.POST.get("Table row")
                tableColumn = request.POST.get("Table column")
                if count_set == 0 :
                    ff.addField(data,label,attr,"form1",0,child="no children")
                    count_set = 1
                else:
                    ff.filename
                    ff.addField(data,label,attr,"form1",1,child="no children")
                return HttpResponse(Filedata(ff.filename))

    def edit_field(request):                
        return HttpResponse(df.fieldConfig())
    
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

    def calculatevalue():
        # called on a result field 
        # this would sipmlify the calculation part 
        # and when save is clicked the value will be saved
        pass
    def link_data_field():
        # the field is linked via varname which is stored in a vartable which is searched for the value and 
        # is poulated to the link destination can be asked by a report or a form 
        # this poses another problem if the link source name is changed the link dest will be floating
        # this should be resolved by throwing error to the user and showing which forms link source is 
        # responsible for the error which  means the vartable has to store the varname and the formname of the varname.
        pass
    def cancel():
        return HttpResponse("")


class report():
    
    def new_report (request):
        pass
    
    def edit_report (request):
        pass

    def summary_view_report():
        pass

    def detail_view_report():
        pass
    
    def delete_report (request):
        pass


class group():
    
    def new_group (request):
        pass
    
    def edit_group (request):
        pass
    
    def delete_group (request):
        pass

class db():
    
    def create_db (request):
        pass
    
    def createtable_db (request):
        pass
    
    def edittable_db (request):
        pass
    
    def deletetable_db (request):
        pass
    
    def backup (request):
        pass

