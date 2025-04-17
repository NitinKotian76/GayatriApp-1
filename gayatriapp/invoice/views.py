from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
import logging
from .cachestore import cachestore as cache
from django.views import View
from .models import *
from .forms import *
# from .formmod.Displayform import DisplayForm as ds
from .formmod import DefaultForm as df
from .formmod import BaseForm as bf

# from .formmod.form_setup import form_config
from django.contrib.auth.models import User
from django import forms

# from .formmod.CrudForm import form_store_json

# NOTE: anything that is returned by the rendered template should be validated
# by the client and then the server

logger = logging.getLogger(__name__)

# decorator = [login_required, permission_required]


def login_user(request):
    if request.method == 'POST':
        form = bf.loginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            logger.debug("logged in")
            return redirect("invoice:index")
    else:
        form = bf.loginForm()
        logger.debug("login password or username failed")
    return render(request, "invoice/login.html", {"login": form})


def index(request):
    logger.debug(request.user.is_active)
    return render(
        request,
        "invoice/index.html",
        {"user": request.user},
    )


class profile_user(View):

    def get(self, request):
        return HttpResponse(df.profilehtml(user.objects.all()))

    def post(self, request):
        logout(request)
        return render(request, "invoice/login.html", {"login": df.logouthtml()})


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


def form_view(request):
    formdata = None
    logger.debug(request.GET.get("form"), df.customer)
    if request.method == "GET":
        logger.debug(request.GET.get("form"), df.customer)
        # masters
        if request.GET.get("form") == "customer":
            formdata = df.customer
        if request.GET.get("form") == "supplier":
            formdata = df.supplier
        if request.GET.get("form") == "signatory":
            formdata = df.signatory
        if request.GET.get("form") == "export_fields":
            formdata = df.export_fields
        if request.GET.get("form") == "item_category":
            formdata = df.item_category
        if request.GET.get("form") == "variety":
            formdata = df.item_category
        if request.GET.get("form") == "items":
            formdata = df.items
        if request.GET.get("form") == "stock":
            formdata = df.stock
        if request.GET.get("form") == "units":
            formdata = df.units
        if request.GET.get("form") == "location":
            formdata = df.location
        # transactions

        if request.GET.get("form") == "open_bal_prod":
            formdata = df.open_bal_prod
        if request.GET.get("form") == "prod_record":
            formdata = df.prod_record
        if request.GET.get("form") == "prod_plus_minus":
            formdata = df.prod_plus_minus
        if request.GET.get("form") == "prod_approval":
            formdata = df.prod_approval
        if request.GET.get("form") == "invoice_direct":
            formdata = df.invoice_direct
        if request.GET.get("form") == "jumbo_roll_qc":
            formdata = df.jumbo_roll_qc
        if request.GET.get("form") == "lot_no_wise_qc":
            formdata = df.lot_no_wise_qc
        if request.GET.get("form") == "finishing_house":
            formdata = df.finishing_house
        if request.GET.get("form") == "programme_planning":
            formdata = df.finishing_house

    return render(request, "partials/forms.html", {"form": formdata})


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
