from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.contrib import messages
import logging
from ..cachestore import cachestore as cache
from ..models import *
from ..forms import *
from ..formmod import DefaultForm as df
from ..formmod import BaseForm as bf
from ..dbmod import dbfunctions as db
from ..reportmod import create_report as cr
from .. import mappings as mp

# IMPROVEMENT NEEDED: Add proper docstring for the module
# IMPROVEMENT NEEDED: Add proper type hints for better code maintainability
# IMPROVEMENT NEEDED: Consider splitting views into separate files (auth_views.py, form_views.py, etc.)

logger = logging.getLogger(__name__)

@login_required
@permission_required('invoice.view_form', raise_exception=True)
def report_view(request):
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
            formdata = handler["form_class"](request.POST, user_id=request.user.id)
            # buttons
            for key in handler["buttons"]:
                hx_vals = handler["buttons"][key]["hx_vals"]
                hx_req = handler["buttons"][key]["hx_req"]
                button = bf.button(key, hx_vals, hx_req)
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