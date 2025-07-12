from django.shortcuts import render, redirect
from django.urls import reverse
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
from ..formmod import Static as df
from ..formmod import Base as bf
from ..dbmod import dbfunctions as db
from ..reportmod import create_report as cr
from .. import mappings as mp
from django.forms import formset_factory

# class based Views

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

# =====================
# PRIORITY 2: CRUD Operations for Admin Views
# These views are placeholders for CRUD operations and will be developed later.
#
# Possible approaches for implementation:
# - Use Django's generic class-based views (ListView, CreateView, UpdateView, DeleteView) for standard CRUD patterns.
# - Leverage form classes in formmod/BaseForm.py and formmod/DefaultForm.py for custom form handling.
# - Integrate with the existing caching and dbfunctions modules for optimized data access and business logic.
# - Ensure proper permission checks using Django's @permission_required decorators.
# - Use partial templates in templates/partials/ for modular UI rendering.
# - Add pagination and search/filtering using Django's Paginator and QuerySet APIs.
# - Implement logging and error handling as per project standards.
#
# NOTE: Actual implementation should follow the project's modular structure and reuse existing utilities where possible.
# =====================

# IMPROVEMENT NEEDED: Add proper docstring for the module
# IMPROVEMENT NEEDED: Add proper type hints for better code maintainability
# IMPROVEMENT NEEDED: Consider splitting views into separate files (auth_views.py, form_views.py, etc.)

# TODO: Implement form_list view
# TODO: Implement report_list view
logger = logging.getLogger(__name__)


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
    keyValueFormset = formset_factory(bf.keyValueForm, extra=1)
    if request.method == 'POST':
        form = bf.new_report(request.POST)
        formset = keyValueFormset(request.POST)
        buttons = bf.button("submit", {}, "/invoice/new_report")
    else:
        logger.debug("create new report")
        form = bf.new_report()
        formset = keyValueFormset()
        buttons = bf.button("submit", {}, "/invoice/new_report")
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

# table


@login_required
def create_table(request):
    # PRIORITY 2: To be implemented (Create Table CRUD operation)
    if request.method == 'POST':
        form = bf.table_create(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table_list')
        else:
            logger.error(f"Form validation failed: {form.errors}")
            messages.error(request, "Form validation failed")
    else:
        form = bf.table_create()
        buttons = bf.buttons()
        formset = formset_factory(bf.keyValueForm, extra=1)

    context = {
        "form": form,
        "buttons": buttons,
        "formset": formset
    }
    return render(request, "partials/createform.html", context)


class Table_list(LoginRequiredMixin, ListView):
    # NOTE: priority 2
    model = TableName
    template_name = "partials/tableview.html"
    context_object_name = "listdata"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.GET.get("company")
        if company_id:
            queryset = TableName.objects.filter(
                company=company_id).values("id", "table_name").order_by("id")
            logger.debug(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["buttons"] = bf.button(
            "select",
            {"form": "adminCompany"},
            "/invoice/admin_company"
        )
        logger.debug(context)
        context["form_name"] = "table_list"
        return context


# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging


def admin_company(request):
    buttons = []
    if request.method == 'POST':
        form = bf.adminCompany(request.POST)
        if form.is_valid():
            company_id = form.cleaned_data['company_name'].id
            logger.debug(company_id)
            request.session['selected_company_id'] = company_id
            messages.success(request, "Company selected successfully")
    else:
        form = bf.adminCompany()
    buttons.append(
        bf.button("select", {"form": "adminCompany"}, "/invoice/admin_company"))
    context = {
        "form": form,
        "buttons": buttons,
    }
    return render(request, "partials/forms.html", context)
