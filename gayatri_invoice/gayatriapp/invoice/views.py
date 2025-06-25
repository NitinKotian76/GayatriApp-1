from .all_views.admin_views import *
from .all_views.form_views import *
from .all_views.auth_views import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.paginator import Paginator
from django.contrib import messages as msg
from django.urls import reverse_lazy
from django.views import View
import logging
from invoice.cachestore import cachestore as cache
from .models import *
from .forms import *
from .formmod import DefaultForm as df
from .formmod import BaseForm as bf
from .dbmod import dbfunctions as db
from .reportmod import create_report as cr
from . import mappings as mp
# IMPROVEMENT NEEDED: Add proper docstring for the module
# IMPROVEMENT NEEDED: Add proper type hints for better code maintainability
# IMPROVEMENT NEEDED: Consider splitting views into separate files (auth_views.py, form_views.py, etc.)

logger = logging.getLogger(__name__)

# Import specific views from the segregated files


@ensure_csrf_cookie
@login_required
def index(request):
    # IMPROVEMENT NEEDED: Use get_object_or_404
    user = CustomUser.objects.get(id=request.user.id)
    logger.debug(request.user.is_active)
    if request.user.is_authenticated:
        messages.success(request, "logged in")
    context = {"user": user, "messages": messages.get_messages(request)}
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