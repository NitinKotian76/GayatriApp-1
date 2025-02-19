from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
import logging
from .cachestore import cachestore as cache
from django.views import View
from .models import *
from .formmod.Displayform import DisplayForm as ds
from .formmod import DefaultForm as df
from .viewclasses.form_views import form_config
from django.contrib.auth.models import User

# anything that is returned by the rendered template should be validated
# by the client and then the server
logger = logging.getLogger(__name__)

decorator = [login_required, permission_required]


class login_user(View):

    def get(self, request):
        logger.debug("login page requested")
        return render(request, "invoice/login.html", {"login": df.loginFormhtml()})

    def post(self, request):
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        company = request.POST.get("Select Company:")
        user = authenticate(request, username=username, password=password)
        logger.debug(company)
        # if modelContains.company  = username :
        #     then login start cookie
        # if usernamme.attempts is not >3
        if user is not None:
            logger.debug("login success")
            login(request, user)
            return redirect("invoice:index")
        else:
            logger.debug("login failed")
            return render(request, "invoice/login.html", {"login": df.loginFailhtml()})


class profile_user(View):

    def get(self, request):
        return HttpResponse(df.profilehtml())

    def post(self, request):
        logout(request)
        return render(request, "invoice/login.html", {"login": df.logouthtml()})


class index(View):

    def get(self, request):
        logger.debug("index page requested")
        return render(request, "invoice/index.html", {"itemlist": df.addFieldshtml()})


class form_setup(View):

    def get(self, request):

        if request.GET.get("view") == "formdelete":
            # show the formconfig
            logger.debug("form delete page requested")
            return HttpResponse(df.formDeletehtml())

        if request.GET.get("view") == "formconfig":
            # show the formconfig
            logger.debug("form config page requested")
            return HttpResponse(df.formConfightml())

        if request.GET.get("view") == "formedit":
            # show the formconfig
            # TODO: check if any form is available and give and option to choose a form show a form list view
            logger.debug("form config page requested for editing")
            return HttpResponse(df.formEdithtml())

    def post(self, request):
        # get the config
        logger.debug("data sent to form setup ")

        formname = request.POST.get("Form Name")
        username = request.POST.get("User Name")
        read = request.POST.get("Read")
        write = request.POST.get("Write")
        tablenames = request.POST.get("Tables")
        description = request.POST.get("Description")
        form_config.create_form(
            formname, username, read, write, tablenames, description
        )

        logger.debug("redirect to field config page")
        # TODO: save in cache
        return HttpResponse(df.addFieldshtml())


class field_setup(View):
    def get(self, request):
        return HttpResponse(df.fieldConfightml())

    def post(self, request):
        fieldtype = request.POST.get("field type")
        label = request.POST.get("Field Name")
        disabled = request.POST.get("Disabled")
        tableRow = request.POST.get("Table Row")
        tableColumn = request.POST.get("Table Column")
        fieldno = cache.get("fieldno")
        add_field(fieldtype, label, attr, form, fieldno, child)
        if field == 0:
            cache.set("fieldno", fieldno + 1)


class user(View):
    def get(self, request):
        pass

    def post(self, request):
        if request.POST.get("view") == "createuser":
            username = request.POST.get("Username")
            password = request.POST.get("Password")
            company = request.POST.get("Select Company")
            User.objects.create(username, password, company, userAccess=None)
        if request.POST.get("view") == "inactiveuser":
            pass
        if request.POST.get("view") == "deleteuser":
            pass


class report(View):
    pass


class db(View):
    pass


# class group():
#
#     def new_group (request):
#         pass
#
#     def edit_group (request):
#         pass
#
#     def delete_group (request):
#         pass
#
