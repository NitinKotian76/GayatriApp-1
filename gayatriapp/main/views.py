from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse 
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .models import UserProfile, Forms
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
import json
from django.core.cache import cache
import logging

from .formmod.Displayform import DisplayForm as ds
from .formmod  import DefaultForm as df
from .formmod.CreateForm import formFieldData
from .formmod.LoadForm import Filedata
from .formmod.ValidateForm import ValidatorInstances as vld

# Create your views here.
# ds = DisplayForm()
        
# anything that is returned by the rendered template should be validated by the client and then the server
logger = logging.getLogger(__name__)
class intro():
    def login(request):
        if request.method == "POST":
            username = request.POST["Username"]
            password = request.POST["Password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                logger.debug("login success")
                login(request,user)
                return redirect("main:index")
            else:
                logger.debug("login failed")
                return render(request,"main/login.html",{"login":df.loginFail()})
        else:
            logger.debug("login page requested")
            return render(request,"main/login.html",{
                "login":df.loginForm()
                }
            )

@login_required
class home():
    def index(request):
        logger.debug("index page requested")
        return render(request,"main/index.html",{"itemlist":df.addFields()})

@login_required
class user():

    def logout_user(request):
        logout(request)
        return render(request,"main/login.html",{"login":df.logedout()})

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
        logger.debug("form config page requested")
        if request.method == "GET":
            return HttpResponse(df.formConfig())

    def form_setup(request):
        # name the form , give permissions , attach tables to the form
        """
        this def gets the input from the form info page and sets up the form data in json
        """
        if request.method == "POST":
            logger.debug("data sent to form setup ")
            formName = request.POST.get("Form Name")
            userName = request.POST.get("User Name")
            read= request.POST.get("Read")
            write= request.POST.get("Write")
            TableNames = request.POST.get("Tables")
            description= request.POST.get("Description")
            Access_rights = {userName:[read,write]} ## username as key to the access rights 
            tables = {"tables":TableNames}
            # if vld.text(userName,100)==None and vld.text(description,400) == None:
            #     logger.debug("validated formconfig ")
            ff=formFieldData(formName,Access_rights,tables) #### this variable is present in the class
            logger.debug("redirect to field config page")
                # response = redirect("main:edit_form") ## this i am doing to display success from the server
            response = redirect("main:edit_form")
            # else:
            #     response = HttpResponseBadRequest("form input error")
            return response

    def save_form(request):
        if request.method == "POST":
            ff.saveForm(ff.FieldDataDict)
            logger.debug("form saved")
            return JsonResponse({"success":True,"message":"form saved successfully"})
    
    def delete_form (request):
         if request.method == "POST":
             return(ff.deleteForm(ff.filename))
    
    def edit_form(request):
         logger.debug(df.addFields())
         return HttpResponse(df.addFields())


    def add_field(request):
        if request.method == "POST":
                label = request.POST.get("Field Name")
                disabled = request.POST.get("Disabled")
                tableRow = request.POST.get("Table Row")
                tableColumn = request.POST.get("Table Column")
                ff.addField(data,label,attr,"form1",0,child="no children")
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


@login_required
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


@login_required
class group():
    
    def new_group (request):
        pass
    
    def edit_group (request):
        pass
    
    def delete_group (request):
        pass

@login_required
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
