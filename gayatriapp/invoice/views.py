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
    methodlist = bf.getInputFields(df)
    if request.method == "GET":
        if request.GET.get("form") == "Company":
            # return render(request, "partials/forms.html", {"form": df.Company})
            return HttpResponse(df.Company)

        if request.GET.get("form") == "CustomUser":
            return render(request, "partials/forms.html", {"form": df.CustomUser})

        if request.GET.get("form") == "CustomUserManager":
            return render(request, "partials/forms.html", {"form": df.CustomUserManager})

        if request.GET.get("form") == "Form":
            return render(request, "partials/forms.html", {"form": df.Form})

        if request.GET.get("form") == "GinIndex":
            return render(request, "partials/forms.html", {"form": df.GinIndex})

        if request.GET.get("form") == "Group":
            return render(request, "partials/forms.html", {"form": df.Group})

        if request.GET.get("form") == "Permission":
            return render(request, "partials/forms.html", {"form": df.Permission})

        if request.GET.get("form") == "PermissionsMixin":
            return render(request, "partials/forms.html", {"form": df.PermissionsMixin})

        if request.GET.get("form") == "Programme_planing":
            return render(request, "partials/forms.html", {"form": df.Programme_planing})

        if request.GET.get("form") == "Report":
            return render(request, "partials/forms.html", {"form": df.Report})

        if request.GET.get("form") == "Table":
            return render(request, "partials/forms.html", {"form": df.Table})

        if request.GET.get("form") == "ValidationError":
            return render(request, "partials/forms.html", {"form": df.ValidationError})

        if request.GET.get("form") == "authenticate":
            return render(request, "partials/forms.html", {"form": df.authenticate})

        if request.GET.get("form") == "customer":
            return render(request, "partials/forms.html", {"form": df.customer})

        if request.GET.get("form") == "export_fields":
            return render(request, "partials/forms.html", {"form": df.export_fields})

        if request.GET.get("form") == "finishing_house":
            return render(request, "partials/forms.html", {"form": df.finishing_house})

        if request.GET.get("form") == "invoice_direct":
            return render(request, "partials/forms.html", {"form": df.invoice_direct})

        if request.GET.get("form") == "item_category":
            return render(request, "partials/forms.html", {"form": df.item_category})

        if request.GET.get("form") == "items":
            return render(request, "partials/forms.html", {"form": df.items})

        if request.GET.get("form") == "jumbo_roll_qc":
            return render(request, "partials/forms.html", {"form": df.jumbo_roll_qc})

        if request.GET.get("form") == "location":
            return render(request, "partials/forms.html", {"form": df.location})

        if request.GET.get("form") == "lot_no_wise_qc":
            return render(request, "partials/forms.html", {"form": df.lot_no_wise_qc})

        if request.GET.get("form") == "open_bal_prod":
            return render(request, "partials/forms.html", {"form": df.open_bal_prod})

        if request.GET.get("form") == "prod_approval":
            return render(request, "partials/forms.html", {"form": df.prod_approval})

        if request.GET.get("form") == "prod_plus_minus":
            return render(request, "partials/forms.html", {"form": df.prod_plus_minus})

        if request.GET.get("form") == "prod_record":
            return render(request, "partials/forms.html", {"form": df.prod_record})

        if request.GET.get("form") == "signatory":
            return render(request, "partials/forms.html", {"form": df.signatory})

        if request.GET.get("form") == "stock":
            return render(request, "partials/forms.html", {"form": df.stock})

        if request.GET.get("form") == "supplier":
            return render(request, "partials/forms.html", {"form": df.supplier})

        if request.GET.get("form") == "units":
            return render(request, "partials/forms.html", {"form": df.units})

    # if request.GET.get("form") =:
    #     return HttpResponse(request, ...)


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
