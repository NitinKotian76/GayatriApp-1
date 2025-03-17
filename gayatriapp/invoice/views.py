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
from .forms import *
from .formmod.Displayform import DisplayForm as ds
from .formmod import DefaultForm as df
from .formmod.form_views import form_config
from django.contrib.auth.models import User
from django import forms

# anything that is returned by the rendered template should be validated
# by the client and then the server
logger = logging.getLogger(__name__)

# decorator = [login_required, permission_required]


def login_user(request):
    form = df.loginForm()
    if request.method == "GET":
        logger.debug("login page requested")
        return render(
            request,
            "invoice/login.html",
            {"login": form},
        )

    if request.method == "POST":
        if form.is_valid():
            empid = form.cleaned_data("empid")
            password = form.cleaned_data("password")
            compname = form.clean_data("cmpname")
            user = authenticate(
                request, user_emp_code=empid, password=password, company=company_name
            )
            if user is not None:
                # logger.debug("login success")
                # if user.company.company_name != compname:
                #     logger.debug("login not from %s ", user.company.company_name)
                #     return render(
                #         request,
                #         "invoice/login.html",
                #         {"login": df.loginFormhtml(Company.objects.all(), 2)},
                #     )
                login(request, user)
                return redirect("invoice:index")
            else:
                logger.debug("login password or username failed")
                return render(
                    request,
                    "invoice/login.html",
                    {"login": form},
                )


class profile_user(View):

    def get(self, request):
        return HttpResponse(df.profilehtml(user.objects.all()))

    def post(self, request):
        logout(request)
        return render(request, "invoice/login.html", {"login": df.logouthtml()})


def index(request):
    logger.debug("index page requested")
    return render(
        request,
        "invoice/index.html",
        {"itemlist": ""},
    )


class form_setup(View):

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


def form_config(request):
    return HttpResponse(df.formConfig())


def form_delete(request):
    return HttpResponse(df.formDeletehtml())


def form_edit(request):
    return HttpResponse(df.formEdithtml())


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


class report(View):
    pass
