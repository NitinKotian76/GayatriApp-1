from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
import logging
from ..cachestore import cachestore as cache
from ..models import *
from ..form_files import *
from ..form_files import Static as df
from ..form_files import Base as bf
from ..form_files import helperFunct as hf
from ..dbmod import dbfunctions as db
from .. import mappings as mp
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
# IMPROVEMENT NEEDED: Add proper docstring for the module
# IMPROVEMENT NEEDED: Add proper type hints for better code maintainability

logger = logging.getLogger(__name__)


@login_required
@permission_required('invoice.view_form', raise_exception=True)
def form_view(request):
    # NOTE: this view is used for general forms
    # IMPROVEMENT NEEDED: Use proper constant naming convention
    form_handler = mp.FORMHANDLER
    formdata = None
    buttons = []
    user_id = request.user.id

    if request.method == "POST":
        formtype = request.POST.get("form")
        logger.debug(request.POST.get('form'))
        if formtype in form_handler:
            handler = form_handler[formtype]
            formdata = handler["form_class"](request.POST, user_id=user_id)
            buttons = hf.btn_append(handler, "buttons")
            logger.debug("get the metadata")
            if formdata.is_valid():
                logger.debug("data validated")
                data = formdata.cleaned_data
                if request.user.is_admin:
                    company_id = request.session.get('selected_company_id')
                if db.set_data(handler["table_name"], data, user_id, company_id):
                    messages.success(request, "data saved")
                else:
                    logger.debug("data is not saved")
                    messages.error(request, "data is not saved")
                formdata = handler["form_class"](request.POST)

    else:
        formtype = request.GET.get("form")
        if formtype in form_handler:
            handler = form_handler[formtype]
            formdata = handler["form_class"](user_id=user_id)
            buttons = hf.btn_append(handler, "buttons")
    context = {
        "form": formdata,
        "buttons": buttons,
        "messages": messages.get_messages(request)
    }

    return render(request, "partials/forms.html", context)

# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging
# IMPROVEMENT NEEDED: Add proper form validation


@ensure_csrf_cookie
@login_required
@never_cache
def table_data_view(request):
    buttons = []
    table_name = request.GET.get("table_name")
    form_name = request.GET.get("form")
    data = None
    rows = []
    page_obj = None
    user_id = request.user.id

    logger.debug(request.GET)

    if form_name and form_name in mp.FORMHANDLER:
        handler = mp.FORMHANDLER[form_name]
        table_name = handler["table_name"]
        if "table_buttons" in handler:
            buttons = hf.btn_append(handler, "table_buttons")
    elif table_name:
        data = db.get_data(table_name, user_id)
    else:
        logger.debug("issue with the request")
        return HttpResponse(status=404)
    # this if is for admin view
    if request.user.is_admin:
        company_id = request.session.get('selected_company_id')
        data = db.get_data(table_name, user_id, company_id)
    else:
        data = db.get_data(table_name, user_id)

    if not data:
        logger.debug("table empty: " + table_name)
        messages.error(request, "table empty: " + table_name)
        # give a empty table
    else:
        paginator = Paginator(data, 20)
        page_number = request.GET.get("page")
        logger.debug(page_number)
        page_obj = paginator.get_page(page_number)
        rows = [{"id": obj.get("id"), "table_data": obj.get(
            "table_data")} for obj in page_obj]
        logger.debug(type(rows))

    context = {
        "rows": rows,
        "page_obj": page_obj,
        "table_name": table_name,
        "form_name": form_name,
        "buttons": buttons
    }
    response = render(request, "partials/tableview.html", context)
    response['Cache-Control'] = 'no-cache, must-revalidate'
    return response

# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging
# IMPROVEMENT NEEDED: Add proper form validation


@login_required
@require_POST
def select_row(request):
    if request.method == "POST":
        row_id = request.POST.get('row_id')
        selected_rows = request.session.get('selected_rows', [])
        # Toggle selection
        if row_id in selected_rows:
            selected_rows.remove(row_id)
            logger.debug(selected_rows)
            logger.debug(row_id)
        else:
            selected_rows.append(row_id)
            logger.debug(selected_rows)
            logger.debug(row_id)

    # Update session
        request.session['selected_rows'] = selected_rows
        request.session.modified = True

    return HttpResponse(status=200)


def reset_selected_row(request):
    request.session["selected_rows"] = []
    return HttpResponse(status=200)


def delete_row(request):
    selected_rows = request.session.get('selected_rows', [])
    # delete selected selected_rows
    for row_id in selected_rows:
        logger.debug(TableData.objects.filter(pk=row_id).delete())
        selected_rows.remove(row_id)
    request.session['selected_rows'] = selected_rows
    return HttpResponse(status=200)


def approve_row(request):
    selected_rows = request.session.get('selected_rows', [])
    logger.debug(selected_rows)
    for row_id in selected_rows:
        data = TableData.objects.filter(pk=row_id).values()
        logger.debug(data)
        # column = list(data)[0]["table_data"]
        # column["approved"] = True
        # data.update(table_data=column)
        # logger.debug("updated", row_id)

    return HttpResponse(status=200)


# forms


@login_required
def form_setup(request):
    # PRIORITY 2: To be implemented (Create Form CRUD operation)
    if request.method == 'POST':
        # get the config
        formdata = bf.create_form(request.POST)
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
    else:
        formdata = bf.create_form()

    context = {}
    return render(request, "partials/formcrud.html", context)
# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging
# IMPROVEMENT NEEDED: Add proper form validation


@login_required
def field_setup(View):  # IMPROVEMENT NEEDED: Fix class inheritance
    # PRIORITY 2: To be implemented (Create Field CRUD operation)
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

# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging


@login_required
def form_config(request):
    # PRIORITY 2: To be implemented (Create Form CRUD operation)
    form = bf.open_bal_prod()
    return render(request, "partials/forms.html", {"form": form})

# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging


@login_required
def form_delete(request):
    # PRIORITY 2: To be implemented (Delete Form CRUD operation)
    form = df.formDelete()
    return render(request, "partials/forms.html", {"form": form})


@login_required
def form_edit(request):
    # PRIORITY 2: To be implemented (Edit Form CRUD operation)
    logger.debug("edit form")


@login_required
def form_list(request):
    # PRIORITY 2: To be implemented (List Forms CRUD operation)
    logger.debug("list form")
