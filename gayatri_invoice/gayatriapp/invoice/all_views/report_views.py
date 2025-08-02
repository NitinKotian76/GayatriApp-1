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
from ..dbmod import dbfunctions as df
from .. import mappings as mp
from django.core.cache import cache

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
        print(request.headers.get('HX-request'))
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


@login_required
def report_list(request):
    # PRIORITY 1: To be implemented (List Reports CRUD operation)
    logger.debug("list report")
# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging


@login_required
def new_report(request):
    # PRIORITY 2: To be implemented (Create Report CRUD operation)
    keyValueFormset = formset_factory(cr.keyValueForm)
    if request.method == 'POST':
        logger.debug(request.FILES)
        form = cr.reportCreate(request.POST, request.FILES)
        formset = keyValueFormset(request.POST)
        buttons = hf.button("submit",
                            hx_req_type="hx-post",
                            hx_req="/invoice/new_report",
                            hx_target="#dynform",
                            hx_swap="innerHTML")
        # do something with the data
        logger.debug(form.errors)
        logger.debug(formset.errors)
        if form.is_valid() and formset.is_valid():
            data = form.cleaned_data
            logger.debug(data)
            tagdata = {}
            for i in range(0, total_forms):
                key = formset.cleaned_data[f"form-{i}-key"]
                value = formset.cleaned_data[f"form-{i}-value"]
                tagdata[key] = value
            logger.debug(tagdata)
    else:
        logger.debug("create new report")
        form = cr.reportCreate()
        formset = keyValueFormset()
        logger.debug(formset.management_form)
        buttons = hf.button("submit",
                            hx_req_type="hx-post",
                            hx_req="/invoice/new_report",
                            hx_target="#dynform",
                            hx_swap="innerHTML")

    context = {"form": form,
               "formset": formset,
               "buttons": buttons,
               "req": "/invoice/formset_view"}
    return render(request, "partials/forms.html", context)

# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging


def add_formset_field(request):
    newform = None
    forms = []
    keyValueFormset = formset_factory(cr.keyValueForm)
    if request.POST.get("add"):
        total_forms = request.POST.get("form-TOTAL_FORMS")
        if total_forms == None:
            total_forms = 1
        else:
            total_forms = int(total_forms)+1

        formset = keyValueFormset(request.POST)
        newform = formset.empty_form
        newform.prefix = f"{formset.prefix}-{total_forms}"
        for form in formset.forms:
            forms.append(form)
        forms.append(newform)

    context = {"formset": forms, "total_forms": total_forms}
    return render(request, "partials/formset.html", context)


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
