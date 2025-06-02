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
from .formmod import DefaultForm as df
from .formmod import BaseForm as bf
from .dbmod import dbfunctions as db
from django.core.paginator import Paginator
from django.contrib import messages
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
        if not request.user.is_authenticated:
            logger.debug("login password or username failed")
    return render(request, "invoice/login.html", {"login": form, "messages": messages.get_messages(request)})


@login_required
def logout_user(request):
    logger.debug("logout")
    logout(request)
    messages.info(request, "logged out")
    return redirect("/invoice")


@login_required
def index(request):
    user = CustomUser.objects.get(id=request.user.id)
    logger.debug(request.user.is_active)
    if request.user.is_authenticated:
        messages.success(request, "logged in")
    return render(
        request,
        "invoice/index.html",
        {"user": user, "messages": messages.get_messages(request)},
    )


@login_required
def form_view(request):
    formdata = None
    buttons = None
    hx_req = 'hx-post="/invoice/form_view"'
    FORMHANDLER = {
        "customer": {
            "form_class": df.customer,
            "table_name": "customer"
        },
        "supplier": {
            "form_class": df.customer,
            "table_name": "supplier"
        },
        "signatory": {
            "form_class": df.signatory,
            "table_name": "signatory"
        },
        "export_fields": {
            "form_class": df.export_fields,
            "table_name": "export_fields"
        },
        "item_category": {
            "form_class": df.item_category,
            "table_name": "item_category"
        },
        "variety": {
            "form_class": df.variety,
            "table_name": "variety"
        },
        "items": {
            "form_class": df.items,
            "table_name": "items"
        },
        "stock": {
            "form_class": df.stock,
            "table_name": "stock"
        },
        "units": {
            "form_class": df.units,
            "table_name": "units"
        },
        "location": {
            "form_class": df.location,
            "table_name": "location"
        },
        "open_bal_prod": {
            "form_class": df.open_bal_prod,
            "table_name": "open_bal_prod"
        },
        "prod_record": {
            "form_class": df.prod_record,
            "table_name": "prod_record"},
        "prod_plus_minus": {
            "form_class": df.prod_plus_minus,
            "table_name": "prod_plus_minus"
        },
        "prod_approval": {
            "form_class": df.prod_approval,
            "table_name": "prod_approval"
        },
        "invoice_direct": {
            "form_class": df.invoice_direct,
            "table_name": "invoice_direct"
        },
        "jumbo_roll_qc": {
            "form_class": df.jumbo_roll_qc,
            "table_name": "jumbo_roll_qc"
        },
        "lot_no_wise_qc": {
            "form_class": df.lot_no_wise_qc,
            "table_name": "lot_no_wise_qc",
        },
        "finishing_house": {
            "form_class": df.finishing_house,
            "table_name": "finishing_house"
        },
        "program_planning": {
            "form_class": df.program_planning,
            "table_name": "program_planning"
        },
    }
    if request.method == "POST":
        formtype = request.POST.get("form")
        logger.debug(formdata)
        if formtype in FORMHANDLER:
            handler = FORMHANDLER[formtype]
            formdata = handler["form_class"](request.POST)
            buttons = df.button(formtype)
            if formdata.is_valid():
                logger.debug("data validated")
                data = formdata.cleaned_data
                user_id = request.user.id
                logger.debug(user_id)
                if db.set_data(handler["able_name"], data, user_id):
                    logger.debug("data is saved")
                    messages.success(request, "data saved")
            else:
                logger.debug("data invalid")
                logger.debug(formdata.errors)
    else:
        formtype = request.GET.get("form")
        if formtype in FORMHANDLER:
            handler = FORMHANDLER[formtype]
            formdata = handler["form_class"]
            buttons = df.button(formtype)

    return render(request, "partials/forms.html", {"form": formdata, "hx_req": hx_req, "buttons": buttons, "messages": messages.get_messages(request)})


@login_required
def table_view(request):
    table_name = request.GET.get("table_name")
    logger.debug(table_name)
    tableinst = TableName.objects.get(table_name=table_name)
    model = TableData.objects.filter(table_name=tableinst).values("table_data")
    paginator = Paginator(list(model), 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "partials/tableview.html", {"page_obj": page_obj})


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
def report_view(request):
    formdata = None
    buttons = None
    hx_req = 'hx-post="/invoice/report_view"'
    if request.method == "POST":
        formdata = request.POST.get("form")
        logger.debug(formdata)
        if request.POST.get("form") == "pendingorder":
            formdata = df.pending_order(request.POST)
            if formdata.is_valid():
                logger.debug("data validated")
                table_name = "pending_order"
                data = formdata.cleaned_data
                user_id = request.user.id
                logger.debug(user_id)
                if db.set_data(table_name, data, user_id):
                    logger.debug("data is saved")
                    messages.info(request, "data saved")
                # TODO: notify the user that data is saved
            else:
                logger.debug("data invalid")
                logger.debug(formdata.errors)
            buttons = df.button("pending_order")
    else:
        # masters
        if request.GET.get("form") == "pendingorder":
            formdata = df.pending_order
            buttons = df.button("pendingorder")
    context = {"form": formdata, "hx_req": hx_req,
               "buttons": buttons, "messages": messages.get_messages(request)}
    return render(request, "partials/forms.html", context)


@login_required
def form_list(request):
    # TODO: form list
    hx_req = 'hx-post="/invoice/report_view"'
    context = {"table": data, "hx_req": hx_req, "buttons": buttons,
               "messages": messages.get_messages(request)}
    return render(request, "partials/forms.html", context)


@login_required
def table_list(request):
    # TODO: form list
    hx_req = 'hx-post="/invoice/report_view"'
    context = {"table": data, "hx_req": hx_req, "buttons": buttons,
               "messages": messages.get_messages(request)}
    return render(request, "partials/forms.html", context)


@login_required
def report_list(request):
    # TODO: form list
    hx_req = 'hx-post="/invoice/report_view"'
    context = {"table": data, "hx_req": hx_req, "buttons": buttons,
               "messages": messages.get_messages(request)}
    return render(request, "partials/forms.html", context)
