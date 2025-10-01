from ..form_files import CrudReport as cr
from ..form_files import CrudTable as ct
from django.shortcuts import render
from django.forms import formset_factory
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages as msg
import logging
from ..models import *
from ..form_files import *

logger = logging.getLogger(__name__)

# mapping
# have to register mappings for the formset
FORMSET_MAP = {
    "reportKeyValueForm": cr.reportKeyValueForm,
    "table_metadata": ct.table_metadata,
}

# common DRY views


def add_formset_field(request, formname: str):
    keyValueForm = FORMSET_MAP.get(formname)
    keyValueFormset = formset_factory(keyValueForm, extra=0)
    if request.method == "POST" and request.POST.get("add"):
        data = request.POST.copy()
        total_forms = int(data.get("form-TOTAL_FORMS", 0))
        data["form-TOTAL_FORMS"] = str(total_forms+1)

        formset = keyValueFormset(data)
    else:
        formset = keyValueFormset()

    context = {"formset": formset, "formset_form": formname}
    return render(request, "partials/formset.html", context)

# other views


@ensure_csrf_cookie
@login_required
def index(request):
    # IMPROVEMENT NEEDED: Use get_object_or_404
    user = CustomUser.objects.get(id=request.user.id)
    logger.debug(request.user.is_active)
    if request.user.is_authenticated:
        msg.success(request, "logged in")
    context = {"user": user, "messages": msg.get_messages(request)}
    return render(request, "invoice/index.html", context)

# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging


@ensure_csrf_cookie
@login_required
def profile_user(request):
    if request.method == 'GET':
        logger.debug(request)
        # IMPROVEMENT NEEDED: Use get_object_or_404
        user = CustomUser.objects.get(user_emp_code=request.user)
        return render(request, "partials/profile.html", {"user": user})

# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging
# IMPROVEMENT NEEDED: Add proper pagination handling


@ensure_csrf_cookie
@login_required
def get_notifications(request):
    messages = msg.get_messages(request)
    if messages:
        return HttpResponse(render_to_string("partials/notif.html", {"messages": messages}))
    return HttpResponse("")
