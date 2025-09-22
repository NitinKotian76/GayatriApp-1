from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
import logging
from ..cachestore import cachestore as cache
from ..models import *
from ..forms import *
from ..formmod import Static as df
from ..formmod import Base as bf
from ..formmod import CrudTable as ct
from ..formmod import helperFunct as hf
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


# table

@login_required
def create_table(request):
    """
        this view is for creating a new table
    """
    metadataform = ct.table_metadata
    formset_metadata = formset_factory(metadataform)
    if request.method == 'POST':
        form = ct.table_create(request.POST)
        formset = formset_metadata(request.POST)
        if form.is_valid():
            pass
        else:
            logger.error(f"Form validation failed: {form.errors}")
            messages.error(request, "Form validation failed")
    else:
        form = ct.table_create()
        buttons = hf.button("submit")
        formset = formset_metadata()

    context = {
        "form": form,
        "formset": formset,
        "formset_form": "table_metadata",
        "buttons": buttons,
    }
    return render(request, "partials/forms.html", context)


def table_list(request):
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
        context["buttons"] = hf.button("select",
                                       hx_req_type="hx-post",
                                       hx_vals={"form": "adminCompany"},
                                       hx_req="/invoice/admin_company",
                                       hx_target="#dynform"
                                       )
        logger.debug(context)
        context["form_name"] = "table_list"
        return context


# IMPROVEMENT NEEDED: Add proper error handling
# IMPROVEMENT NEEDED: Add proper logging


def admin_company(request):
    buttons = []
    if request.method == 'POST':
        form = df.adminCompany(request.POST)
        if form.is_valid():
            company_id = form.cleaned_data['company_name'].id
            logger.debug(company_id)
            request.session['selected_company_id'] = company_id
            messages.success(request, "Company selected successfully")
    else:
        form = df.adminCompany()
    buttons.append(
        hf.button("select",
                  hx_req_type="hx-post",
                  hx_vals={"form": "adminCompany"},
                  hx_req="/invoice/admin_company",
                  hx_target="#dynform"
                  )
    )
    context = {
        "form": form,
        "buttons": buttons,
    }
    return render(request, "partials/forms.html", context)
