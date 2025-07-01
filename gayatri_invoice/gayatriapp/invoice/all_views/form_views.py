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
from ..forms import *
from ..formmod import Static as df
from ..formmod import Base as bf
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
    hx_req = "/invoice/form_view"
    if request.method == "POST":
        formtype = request.POST.get("form")
        logger.debug(formtype)
        if formtype in form_handler:
            handler = form_handler[formtype]
            formdata = handler["form_class"](request.POST)
            for key in handler["buttons"]:
                hx_vals = handler["buttons"][key]["hx_vals"]
                hx_req = handler["buttons"][key]["hx_req"]
                button = bf.button(key, hx_vals, hx_req)
                buttons.append(button)
            if formdata.is_valid():
                logger.debug("data validated")
                data = formdata.cleaned_data
                if request.user.is_admin:
                    company_id = request.session.get('selected_company_id')
                user_id = request.user.id
                logger.debug(user_id)
                if not db.set_data(handler["table_name"], data, user_id, company_id):
                    logger.debug("data is saved")
                    messages.success(request, "data saved")
                else:
                    logger.debug("data is not saved")
                    messages.error(request, "data is not saved")
                formdata = handler["form_class"]()
            else:
                logger.debug("data invalid")
                logger.debug(formdata.errors)
    else:
        formtype = request.GET.get("form")
        if formtype in form_handler:
            handler = form_handler[formtype]
            formdata = handler["form_class"]()
            for key in handler["buttons"]:
                hx_vals = handler["buttons"][key]["hx_vals"]
                hx_req = handler["buttons"][key]["hx_req"]
                button = bf.button(key, hx_vals, hx_req)
                buttons.append(button)
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

    if form_name and form_name in mp.FORMHANDLER:
        handler = mp.FORMHANDLER[form_name]
        table_name = handler["table_name"]
        if "table_buttons" in handler:
            for key in handler["table_buttons"]:
                hx_vals = handler["table_buttons"][key]["hx_vals"]
                hx_req = handler["table_buttons"][key]["hx_req"]
                button = bf.button(key, hx_vals, hx_req)
                buttons.append(button)
        logger.debug("form_name: " + form_name)
    else:
        logger.debug("issue with the request")
        return HttpResponse(status=404)
    # this if is for admin view
    if request.user.is_admin:
        company_id = request.session.get('selected_company_id')

    user_id = request.user.id
    data = db.get_data(table_name, user_id, company_id)
    if not data:
        logger.debug("table name doesnt exist: " + table_name)
        messages.error(request, "table name doesnt exist: " + table_name)
    elif data == []:
        messages.error(request, "table name exists but no data: " + table_name)
    else:
        logger.debug(data)
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
        logger.debug(selected_rows)
        # Toggle selection
        if row_id in selected_rows:
            selected_rows.remove(row_id)
        else:
            selected_rows.append(row_id)
        logger.debug(selected_rows)

    # Update session
        request.session['selected_rows'] = selected_rows
        request.session.modified = True

    return HttpResponse(status=200)


def get_selected_rows(request):
    return request.session.get('selected_rows', [])
