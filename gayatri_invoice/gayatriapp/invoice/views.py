from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth import login, logout
from django.views import View
import logging
from .cachestore import cachestore as cache
from .models import *
from .forms import *
from .formmod.Displayform import DisplayForm as ds
from .formmod import DefaultForm as df
from .formmod import BaseForm as bf
from .dbmod import dbfunctions as db
# from .formmod.CrudForm import form_store_json


# NOTE: anything that is returned by the rendered template should be validated
# by the client and then the server

logger = logging.getLogger(__name__)

login_decorator = [login_required, permission_required]


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


@login_required
def logout_user(request):
    logger.debug("logout")
    logout(request)
    return redirect("/invoice")


@login_required
def index(request):
    logger.debug(request.user.is_active)
    return render(
        request,
        "invoice/index.html",
        {"user": request.user},
    )


@login_required
def form_view(request):
    formdata = None
    buttons = None
    if request.method == "POST":
        formdata = request.POST.get("form")
        logger.debug(formdata)
        if request.POST.get("form") == "customer":
            formdata = df.customer(request.POST)
            logger.debug("data received")

            if formdata.is_valid():
                logger.debug("data validated")
                table_name = "customer"
                data = formdata.cleaned_data
                user_id = request.user.id
                logger.debug(user_id)
                db.set_data(table_name, data, user_id)
                logger.debug("data is saved")
                logger.debug(user_id)

                # TODO: notify the user that data is saved
            else:
                logger.debug("data invalid")
                logger.debug(formdata.errors)
                buttons = df.button("customer")

        if request.POST.get("form") == "supplier":
            formdata = df.supplier(request.POST)
        if request.POST.get("form") == "signatory":
            formdata = df.signatory(request.POST)
        if request.POST.get("form") == "export_fields":
            formdata = df.export_fields(request.POST)
        if request.POST.get("form") == "item_category":
            formdata = df.item_category(request.POST)
        if request.POST.get("form") == "variety":
            formdata = df.item_category(request.POST)
        if request.POST.get("form") == "items":
            formdata = df.items(request.POST)
        if request.POST.get("form") == "stock":
            formdata = df.stock(request.POST)
        if request.POST.get("form") == "units":
            formdata = df.units(request.POST)
        if request.POST.get("form") == "location":
            formdata = df.location(request.POST)
        # transactions

        if request.POST.get("form") == "open_bal_prod":
            formdata = df.open_bal_prod(request.POST)
        if request.POST.get("form") == "prod_record":
            formdata = df.prod_record(request.POST)
        if request.POST.get("form") == "prod_plus_minus":
            formdata = df.prod_plus_minus(request.POST)
        if request.POST.get("form") == "prod_approval":
            formdata = df.prod_approval(request.POST)
        if request.POST.get("form") == "invoice_direct":
            formdata = df.invoice_direct(request.POST)
        if request.POST.get("form") == "jumbo_roll_qc":
            formdata = df.jumbo_roll_qc(request.POST)
        if request.POST.get("form") == "lot_no_wise_qc":
            formdata = df.lot_no_wise_qc(request.POST)
        if request.POST.get("form") == "finishing_house":
            formdata = df.finishing_house(request.POST)
        if request.POST.get("form") == "programme_planning":
            formdata = df.finishing_house(request.POST)

    else:
        # masters
        if request.GET.get("form") == "customer":
            formdata = df.customer
            # table = df.tableview(db.customer)
            buttons = df.button("customer")
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

    return render(request, "partials/forms.html", {"form": formdata, "buttons": buttons})


@login_required
def profile_user(request):

    if request.method == 'GET':
        logger.debug(request)
        user = CustomUser.objects.get(user_emp_code=request.user)
        return render(request, "partials/profile.html", {"user": user})


@login_required
def form_setup(request):

    if request.method == 'POST':
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


@login_required
def field_setup(View):
    if request.method == 'GET':
        return HttpResponse(df.fieldConfightml())

    if request.method == 'POST':
        fieldtype = request.POST.get("field type")
        label = request.POST.get("Field Name")
        disabled = request.POST.get("Disabled")
        tableRow = request.POST.get("Table Row")
        tableColumn = request.POST.get("Table Column")
        fieldno = cache.get("fieldno")
        # add_field(fieldtype, label, attr, form, fieldno, child)
        if fieldno == 0:
            cache.set("fieldno", fieldno + 1)


@login_required
def form_config(request):
    # form = df.formCreate()
    form = bf.open_bal_prod()
    return render(request, "partials/forms.html", {"form": form})


@login_required
def form_delete(request):
    form = df.formDelete()
    return render(request, "partials/forms.html", {"form": form})


@login_required
def form_edit(request):
    form = df.formEdit()
    return render(request, "partials/forms.html", {"form": form})


@login_required
def report(View):
    pass
