from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
import logging
from .cachestore import cachestore as cache
from django.views import View
from .models import *
from .forms import *
from .formmod.Displayform import DisplayForm as ds
from .formmod import DefaultForm as df
from .formmod import BaseForm as bf

# from .formmod.form_setup import form_config
from django.contrib.auth.models import User
from django import forms

from .formmod.CrudForm import form_store_json

# anything that is returned by the rendered template should be validated
# by the client and then the servern
logger = logging.getLogger(__name__)

# decorator = [login_required, permission_required]


def login_user(View):
    def post(self, request):
        form = df.loginForm(request.POST)
        if form.is_valid():
            login(request, form.user())
            logger.debug("logged in")
            return redirect("invoice:index")
        else:
            logger.debug("login password or username failed")
            return render(
                request,
                "invoice/login.html",
                {"login": form},
            )

    def get(self, request):
        form = df.loginForm()
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


@login_required
def index(request):
    logger.debug("index page requested")
    return render(
        request,
        "invoice/index.html",
        {"": ""},
    )


class form_setup(View):

    def post(self, request):
        # get the config
        logger.debug("data sent to form setup ")

        formname = "Form Name"
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
    # form = df.formCreate()
    form = bf.open_bal_prod()
    return render(request, "partials/forms.html", {"form": form})


def form_delete(request):
    form = df.formDelete()
    return render(request, "partials/forms.html", {"form": form})


def form_edit(request):
    form = df.formEdit()
    return render(request, "partials/forms.html", {"form": form})


def forms_view(request):
    return render(request, "partials/table.html", {"table": Table})


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
        # add_field(fieldtype, label, attr, form, fieldno, child)
        if fieldno == 0:
            cache.set("fieldno", fieldno + 1)


class report(View):
    pass
