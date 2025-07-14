from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.forms import formset_factory
import logging
from ..cachestore import cachestore as cache
from ..models import *
from ..forms import *
from ..formmod import CrudReport as cr
from ..formmod import helperFunct as hf
from .. import mappings as mp

# IMPROVEMENT NEEDED: Add proper docstring for the module
# IMPROVEMENT NEEDED: Add proper type hints for better code maintainability
# IMPROVEMENT NEEDED: Consider splitting views into separate files (auth_views.py, form_views.py, etc.)

logger = logging.getLogger(__name__)


@login_required
@permission_required('invoice.view_form', raise_exception=True)
def report_view(request):
    # NOTE: this view is specifically for reports
    # IMPROVEMENT NEEDED: Use proper constant naming convention
    form_handler = mp.REPORT
    formdata = None
    buttons = []
    hx_req = "/invoice/report_view"
    if request.method == "POST":
        formtype = request.POST.get("form")
        logger.debug(formtype)
        if formtype in form_handler:
            handler = form_handler[formtype]
            formdata = handler["form_class"](
                request.POST, user_id=request.user.id)
            # buttons
            for key in handler["buttons"]:
                hx_vals = handler["buttons"][key]["hx_vals"]
                hx_req = handler["buttons"][key]["hx_req"]
                button = hf.button(key, hx_vals, hx_req)
                buttons.append(button)
            # data validation
            if formdata.is_valid():
                logger.debug("data validated")
                data = formdata.cleaned_data
                user_id = request.user.id
                logger.debug(user_id)
            else:
                logger.debug("data invalid")
                logger.debug(formdata.errors)
    else:
        formtype = request.GET.get("form")
        if formtype in form_handler:
            handler = form_handler[formtype]
            formdata = handler["form_class"](user_id=request.user.id)
            for key in handler["buttons"]:
                hx_vals = handler["buttons"][key]["hx_vals"]
                hx_req = handler["buttons"][key]["hx_req"]
                button = hf.button(key, hx_vals, hx_req)
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
# report


@login_required
def report_list(request):
    # PRIORITY 2: To be implemented (List Reports CRUD operation)
    logger.debug("list report")
# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging


@login_required
def new_report(request):
    # PRIORITY 2: To be implemented (Create Report CRUD operation)
    form = cr.new_report()
    keyno = request.session["keyno"]
    keyValueFormset = formset_factory(cr.keyValueForm, extra=keyno)
    if request.method == 'POST':
        form = bf.new_report(request.POST)
        formset = keyValueFormset(request.POST)
        buttons = hf.button("submit", {}, "/invoice/new_report")
    else:
        logger.debug("create new report")
        form = cr.new_report()
        formset = keyValueFormset()
        buttons = hf.button("submit", {}, "/invoice/new_report")
    context = {"form": form, "formset": formset, "buttons": buttons}
    return render(request, "partials/forms.html", context)

# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging


@login_required
def edit_report(request):
    # PRIORITY 2: To be implemented (Edit Report CRUD operation)
    logger.debug("edit report")

# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging


@login_required
def del_report(request):
    # PRIORITY 2: To be implemented (Delete Report CRUD operation)
    pass

# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging
