from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DeleteView, ListView, FormView, View)
from django.urls import (reverse_lazy, reverse)
from django_htmx.http import trigger_client_event
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db.models.functions import Cast
from django.db.models import CharField
from django.db.models import Q, F
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils.html import format_html
from urllib.parse import urlparse, parse_qs

from .services import (
    _set_invoice_productions_out_of_stock,
    _set_invoice_details,
)
from ...form_files import (helperFunct as hf, millsoftForm as mf)
from ...models import (TExport, TExportDetails,
                       TInvoice, TProduction,
                       TProductionReel, MItem)
import logging
logger = logging.getLogger(__name__)


class TExport_create(SuccessMessageMixin, CreateView):

    model = TExport
    form_class = mf.TExportForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TExport_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit",
                                       value="submit",
                                       hx_req=reverse(
                                           'invoice:TExport_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML",
                                       )
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

class TExport_update(SuccessMessageMixin, UpdateView):

    model = TExport
    form_class = mf.TExportForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TExport_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit",
                                       value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML",
                                       )

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

class TExport_delete(SuccessMessageMixin, DeleteView):

    model = TExport
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TExport_list')

class TExport_list(SuccessMessageMixin, ListView):

    model = TExport
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TExport.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TExport_list')
        return context

class TExportDetails_create(SuccessMessageMixin, CreateView):

    model = TExportDetails
    form_class = mf.TExportDetailsForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TExportDetails_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit",
                                       value="submit",
                                       hx_req=reverse(
                                           'invoice:TExportDetails_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML",
                                       )
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

class TExportDetails_update(SuccessMessageMixin, UpdateView):

    model = TExportDetails
    form_class = mf.TExportDetailsForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TExportDetails_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit",
                                       value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML",
                                       )

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

class TExportDetails_delete(SuccessMessageMixin, DeleteView):

    model = TExportDetails
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TExportDetails_list')

class TExportDetails_list(SuccessMessageMixin, ListView):

    model = TExportDetails
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TExportDetails.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TExportDetails_list')
        return context

class TInvoice_create(SuccessMessageMixin, CreateView):

    model = TInvoice
    form_class = mf.TInvoiceForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TInvoice_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        btn = { 
            "buttons": {
                "submit": {
                    "type": "submit",
                    "value": "submit",
                    "hx_req": reverse('invoice:TInvoice_create'),
                    "hx_target": "#dynform",
                    "hx_swap": "innerHTML",
                },
                "challan": {
                    "type": "button",
                    "value": "Challan",
                    "hx_req": reverse('invoice:RChallanCreateView'),
                    "hx_swap": "none",
                },
                "invoice": {
                    "type": "button",
                    "value": "Invoice",
                    "hx_req": reverse('invoice:RInvoiceCreateView'),
                    "hx_swap": "none",
                },
                "gate_pass": {
                    "type": "button",
                    "value": "Gate Pass",
                    "hx_req": reverse('invoice:RGatePassCreateView'),
                    "hx_swap": "none",
                },
            }
        }
        context["buttons"] = hf.btn_append(btn, "buttons")
        return context

    def form_valid(self, form):
        form.save()
        # Remove linked Production records from stock (stk=False) when invoice is created
        _set_invoice_productions_out_of_stock(form.instance)
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

class TInvoice_update(SuccessMessageMixin, UpdateView):

    model = TInvoice
    form_class = mf.TInvoiceForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TInvoice_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = [
            hf.button(type="submit", value="submit", hx_req=f"{self.request.path}", hx_target="#dynform", hx_swap="innerHTML"),
        ]

        return context

    def form_valid(self, form):
        form.save()
        # Remove linked Production records from stock when invoice is updated (e.g. details added)
        _set_invoice_productions_out_of_stock(form.instance)
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

class TInvoice_delete(SuccessMessageMixin, DeleteView):

    model = TInvoice
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TInvoice_list')

@method_decorator(never_cache, name='dispatch')
class TInvoice_list(SuccessMessageMixin, ListView):

    model = TInvoice
    exclude = ["invoiceid", "apiflag", "fac", "stk"] 
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TInvoice.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context["modelurl"] = reverse('invoice:TInvoice_list')
        return context
    
class TProduction_create(SuccessMessageMixin, CreateView):

    model = TProduction
    form_class = mf.TProductionForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TProduction_create")
    success_message = "successfully created"

    def _get_reel_numbers(self, excise_from, excise_to, max_preview=50):
        """Return list of reel numbers from excise_from to excise_to (inclusive). Capped for preview."""
        try:
            start = int(excise_from) if excise_from else 0
            end = int(excise_to) if excise_to else start
            if start <= end:
                count = end - start + 1
                if count <= max_preview:
                    return list(range(start, end + 1))
                return list(range(start, start + max_preview))  # Show first N
        except (ValueError, TypeError):
            pass
        return []

    def _get_dynamic_form_data(self, data):
        """Build form data with preserved user values and computed size, gsm, weight, excise fields."""
        form_data = data.copy()
        if hasattr(form_data, '_mutable'):
            form_data._mutable = True

        itemcode_val = data.get("itemcode", "")
        noofbdls = data.get("noofbdls", "")
        noofream = data.get("noofream", "")
        reamwt = data.get("reamwt", "")
        size = data.get("size", "")
        gsm = data.get("gsm", "")
        noofsheet = data.get("noofsheet", "")
        length = data.get("length", "")
        type_of_reel_sheet = data.get("type_of_reel_sheet", "")

        # Get MItem by pk (ForeignKey value) or by itemcode string
        itemcode_obj = None
        if itemcode_val:
            try:
                itemcode_obj = MItem.objects.get(pk=itemcode_val)
            except (MItem.DoesNotExist, ValueError):
                itemcode_obj = MItem.objects.filter(itemcode=itemcode_val).first()

        if itemcode_obj:
            form_data["size"] = itemcode_obj.size or ""
            form_data["gsm"] = itemcode_obj.gsm or ""
        
        # reamwt (ind_weight) is only calculated when type is not REEL
        if type_of_reel_sheet != "REEL" and size and gsm and noofsheet and length:
            try:
                sheet_area = float(size) * float(length)/10000 # if in cm then convert to m
                form_data["reamwt"] = str(int(sheet_area * float(gsm))* int(noofsheet)/1000) # in kg
            except (ValueError, TypeError):
                pass

        if reamwt and noofream:
            try:
                r = float(reamwt) if str(reamwt).strip() else 0
                n = float(noofream) if str(noofream).strip() else 0
                b = float(noofbdls) if str(noofbdls).strip() else 0
                if r and n:
                    form_data["weight"] = str(int(r * n * b))
            except (ValueError, TypeError):
                pass

        last_reel = TProductionReel.objects.last()
        base_reelno = int(last_reel.reelno) + 1 if last_reel else 1
        form_data["excise_from"] = str(base_reelno)
        if noofbdls:
            try:
                form_data["excise_to"] = str(base_reelno + int(float(noofbdls)))
            except (ValueError, TypeError):
                form_data["excise_to"] = str(base_reelno)

        return form_data

    def get(self, request, *args, **kwargs):
        if request.htmx and request.GET:
            # HTMX change event (itemcode, noofbdls, noofream, reamwt) - preserve form data
            form_data = self._get_dynamic_form_data(request.GET)
            form = self.form_class(data=form_data)
            weight = form_data.get("weight", "")
            noofbdls = form_data.get("noofbdls", "")
            noofream = form_data.get("noofream", "")
            reamwt = form_data.get("reamwt", "")
            try:
                reamwt_int = int(float(reamwt)) if reamwt else 0
                noofream_int = int(float(noofream)) if noofream else 0
                weight_per_row = reamwt_int * noofream_int
                noofbdls_per_row = 1
                noofream_per_row = noofream_int
            except (ValueError, TypeError):
                weight_per_row = reamwt_int * noofream_int
                noofbdls_per_row = 1
                noofream_per_row = 0
            reel_numbers = self._get_reel_numbers(
                form_data.get("excise_from"),
                form_data.get("excise_to"),
            )
            excise_from = form_data.get("excise_from") or 0
            excise_to = form_data.get("excise_to") or excise_from
            try:
                reel_total = int(excise_to) - int(excise_from) + 1 if excise_from and excise_to else len(reel_numbers)
            except (ValueError, TypeError):
                reel_total = len(reel_numbers)
            context = {
                "form": form,
                "buttons": hf.button(
                    type="submit",
                    value="submit",
                    hx_req=reverse("invoice:TProduction_create"),
                    hx_target="#dynform",
                    hx_swap="innerHTML"),
                "reel_numbers": reel_numbers,
                "reel_total": reel_total,
            }
            form_html = render_to_string(self.template_name, context, request=request)
            preview_html = render_to_string(
                "partials/reel_preview.html",
                {
                    "reel_numbers": reel_numbers, 
                    "reel_total": reel_total,
                    "weight": weight,
                    "noofbdls_per_row": noofbdls_per_row,
                    "noofream_per_row": noofream_per_row,
                    "reamwt_per_row": reamwt_int,
                    "weight_per_row": weight_per_row,
                },
                request=request,
            )
            return HttpResponse(form_html + preview_html)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit",
                                       value="submit",
                                       hx_req=reverse(
                                           'invoice:TProduction_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML",
                                       attrs={"hx-confirm": "Are you sure you want to create these reels?"},
                                       )
        return context

    def form_valid(self, form):
        production = form.save(commit=False)
        # reamwt is the ind_weight (individual weight of the bundle)
        if production.reamwt is not None:
            production.ind_weight = production.reamwt
        production.save()
        form.save_m2m()
        excise_from = production.excise_from or 0
        excise_to = production.excise_to or excise_from
        for reelno in range(int(excise_from), int(excise_to) + 1):
            TProductionReel.objects.create(
                productionid=production,
                reelno=reelno,
                stkdate=production.rdate,
            )
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

class TProduction_delete(SuccessMessageMixin, DeleteView):

    model = TProduction
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TProduction_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Delete associated TProductionReel rows so they are not orphaned
        TProductionReel.objects.filter(productionid=self.object).delete()
        return super().delete(request, *args, **kwargs)

@method_decorator(never_cache, name='dispatch')
class TProduction_list(SuccessMessageMixin, ListView):

    model = TProduction
    exclude = ["productionid", "apiflag", "fac", "stk", 
                "approved", "entrytype", "headid","ind_weight",
                "obflag","refproductionid",]
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TProduction.objects.select_related(
            'agentid', 'custid', 'category', 'itemcode', 'shadecode'
        ).annotate(
            pk_str=Cast("pk", output_field=CharField()),
        ).values()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context["modelurl"] = reverse('invoice:TProduction_list')
        if self.request.GET.get("show_reel_button", "false") == "true":
            context["show_reel_button"] = True
        else:
            context["show_reel_button"] = False
        return context

class TStockplusminus(SuccessMessageMixin, FormView):
    """Landing when user opens Stock Plus/minus without selecting a production."""
    template_name = "partials/forms.html"
    form_class = mf.TProductionForm
    context_object_name = "form"
    success_url = reverse_lazy('invoice:TStockplusminus')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit",
                                       value="submit",
                                       hx_req=reverse(
                                           'invoice:TStockplusminus'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML"),
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

class TStockplusminus_update(SuccessMessageMixin, UpdateView):
    """
    Loads form for the selected production; on submit creates a new TProduction
    with refproductionid set to the selected (original) production, plus new
    TProductionReel rows matching the (possibly reduced) excise_from/excise_to.
    Reel preview works like TProduction_create: HTMX GET with form params returns
    form + reel_preview fragment.
    """
    model = TProduction
    form_class = mf.TProductionForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "New production record created with correction."
    success_url = reverse_lazy('invoice:TStockplusminus')

    def _get_reel_numbers(self, excise_from, excise_to, max_preview=50):
        """Return list of reel numbers from excise_from to excise_to (inclusive). Capped for preview."""
        try:
            start = int(excise_from) if excise_from else 0
            end = int(excise_to) if excise_to else start
            if start <= end:
                count = end - start + 1
                if count <= max_preview:
                    return list(range(start, end + 1))
                return list(range(start, start + max_preview))  # Show first N
        except (ValueError, TypeError):
            pass
        return []

    def _get_dynamic_form_data(self, data):
        """Build form data with preserved user values and computed size, gsm, weight, excise fields."""
        form_data = data.copy()
        if hasattr(form_data, '_mutable'):
            form_data._mutable = True

        itemcode_val = data.get("itemcode", "")
        noofbdls = data.get("noofbdls", "")
        noofream = data.get("noofream", "")
        reamwt = data.get("reamwt", "")
        size = data.get("size", "")
        gsm = data.get("gsm", "")
        noofsheet = data.get("noofsheet", "")
        length = data.get("length", "")
        type_of_reel_sheet = data.get("type_of_reel_sheet", "")

        # Get MItem by pk (ForeignKey value) or by itemcode string
        itemcode_obj = None
        if itemcode_val:
            try:
                itemcode_obj = MItem.objects.get(pk=itemcode_val)
            except (MItem.DoesNotExist, ValueError):
                itemcode_obj = MItem.objects.filter(itemcode=itemcode_val).first()

        if itemcode_obj:
            form_data["size"] = itemcode_obj.size or ""
            form_data["gsm"] = itemcode_obj.gsm or ""
        
        # reamwt (ind_weight) is only calculated when type is not REEL
        if type_of_reel_sheet != "REEL" and size and gsm and noofsheet and length:
            try:
                sheet_area = float(size) * float(length)/10000 # if in cm then convert to m
                form_data["reamwt"] = str(int(sheet_area * float(gsm))* int(noofsheet)/1000) # in kg
            except (ValueError, TypeError):
                pass

        if reamwt and noofream:
            try:
                r = float(reamwt) if str(reamwt).strip() else 0
                n = float(noofream) if str(noofream).strip() else 0
                b = float(noofbdls) if str(noofbdls).strip() else 0
                if r and n:
                    form_data["weight"] = str(int(r * n * b))
            except (ValueError, TypeError):
                pass

        last_reel = TProductionReel.objects.last()
        base_reelno = int(last_reel.reelno) + 1 if last_reel else 1
        form_data["excise_from"] = str(base_reelno)
        if noofbdls:
            try:
                form_data["excise_to"] = str(base_reelno + int(float(noofbdls)))
            except (ValueError, TypeError):
                form_data["excise_to"] = str(base_reelno)

        return form_data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["htmx_get_url"] = self.request.path
        return kwargs

    def get(self, request, *args, **kwargs):
        if request.htmx and request.GET:
            form_data = self._get_dynamic_form_data(request.GET)
            form = self.form_class(data=form_data)
            weight = form_data.get("weight", "")
            noofbdls = form_data.get("noofbdls", "")
            noofream = form_data.get("noofream", "")
            reamwt = form_data.get("reamwt", "")
            try:
                reamwt_int = int(float(reamwt)) if reamwt else 0
                noofream_int = int(float(noofream)) if noofream else 0
                weight_per_row = reamwt_int * noofream_int
                noofbdls_per_row = 1
                noofream_per_row = noofream_int
            except (ValueError, TypeError):
                weight_per_row = reamwt_int * noofream_int
                noofbdls_per_row = 1
                noofream_per_row = 0
            reel_numbers = self._get_reel_numbers(
                form_data.get("excise_from"),
                form_data.get("excise_to"),
            )
            excise_from = form_data.get("excise_from") or 0
            excise_to = form_data.get("excise_to") or excise_from
            try:
                reel_total = int(excise_to) - int(excise_from) + 1 if excise_from and excise_to else len(reel_numbers)
            except (ValueError, TypeError):
                reel_total = len(reel_numbers)

            reel_preview_context = {
                "reel_numbers": reel_numbers,
                "reel_total": reel_total,
                "weight": weight,
                "noofbdls_per_row": noofbdls_per_row,
                "noofream_per_row": noofream_per_row,
                "reamwt_per_row": reamwt_int,
                "weight_per_row": weight_per_row,
            }

        else:
            self.object = self.get_object()
            form = self.get_form()
            excise_from = getattr(self.object, "excise_from", None)
            excise_to = getattr(self.object, "excise_to", None)
            reel_numbers = self._get_reel_numbers(excise_from, excise_to)
            try:
                ef = int(excise_from) if excise_from else 0
                et = int(excise_to) if excise_to else ef
                reel_total = et - ef + 1 if ef <= et else len(reel_numbers)
            except (ValueError, TypeError):
                reel_total = len(reel_numbers)
            weight = getattr(self.object, "weight", None)
            noofbdls = getattr(self.object, "noofbdls", None)
            noofream = getattr(self.object, "noofream", None)
            reamwt = getattr(self.object, "reamwt", None)
            try:
                reamwt_int = int(float(reamwt)) if reamwt else 0
                noofream_int = int(float(noofream)) if noofream else 0
                weight_per_row = reamwt_int * noofream_int
                noofbdls_per_row = 1
                noofream_per_row = noofream_int
            except (ValueError, TypeError):
                weight_per_row = reamwt_int * noofream_int
                noofbdls_per_row = 1
                noofream_per_row = 0

            reel_preview_context = {
                "reel_numbers": reel_numbers,
                "reel_total": reel_total,
                "weight": weight,
                "noofbdls_per_row": noofbdls_per_row,
                "noofream_per_row": noofream_per_row,
                "reamwt_per_row": reamwt_int,
                "weight_per_row": weight_per_row,
            }


        context = {
            "form": form,
            "buttons": hf.button(
                type="submit", value="submit",
                hx_req=self.request.path,
                hx_target="#dynform",
                hx_swap="innerHTML"),
            **reel_preview_context
        }
        form_html = render_to_string(self.template_name, context, request=request)
        preview_html = render_to_string(
            "partials/reel_preview.html",
            reel_preview_context,
            request=request,
        )
        return HttpResponse(form_html + preview_html)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(
            type="submit", value="submit",
            hx_req=f"{self.request.path}",
            hx_target="#dynform",
            hx_swap="innerHTML"
        )
        return context

    def form_valid(self, form):
        original = self.object
        # Capture original PK before we mutate the instance (form instance is the same object as original)
        original_productionid = original.productionid
        # Create new TProduction from form, do not update the original
        new_production = form.save(commit=False)
        new_production.pk = None
        new_production.productionid = None
        new_production.refproductionid = original_productionid
        if new_production.reamwt is not None:
            new_production.ind_weight = new_production.reamwt
        new_production.save()
        form.save_m2m()
        # Create TProductionReel rows for the new production (match excise_from/excise_to)
        excise_from = new_production.excise_from or 0
        excise_to = new_production.excise_to or excise_from
        for reelno in range(int(excise_from), int(excise_to) + 1):
            TProductionReel.objects.create(
                productionid=new_production,
                reelno=reelno,
                stkdate=new_production.rdate,
            )
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

class TProductionReel_create(SuccessMessageMixin, CreateView):

    model = TProductionReel
    form_class = mf.TProductionReelForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TProductionReel_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit",
                                       value="submit",
                                       hx_req=reverse(
                                           'invoice:TProductionReel_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML"),
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshReelview", after="settle")

class TProductionReel_update(SuccessMessageMixin, UpdateView):

    model = TProductionReel
    form_class = mf.TProductionReelForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TProductionReel_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit",
                                       value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML"),

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshReelview", after="settle")

class TProductionReel_delete(SuccessMessageMixin, DeleteView):

    model = TProductionReel
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TProductionReel_list')

class TProductionReel_list(SuccessMessageMixin, ListView):

    model = TProductionReel
    exclude = ["productionreelid", "apiflag", "fac", "stk"]
    context_object_name = "form"
    template_name = "partials/reelview.html"
    paginate_by = 100

    def get_queryset(self):
        qs = TProductionReel.objects.annotate(
            pk_str=Cast("pk", output_field=CharField())
        )
        production_id = self.request.GET.get("production")
        custid = self.request.GET.get("custid")
        agentid = self.request.GET.get("agentid")
        if production_id:
            qs = qs.filter(productionid_id=production_id)
        else:
            # Invoice context: reels from productions for this party and/or agent (in stock only)
            if custid or agentid:
                qs = qs.filter(productionid__stk=True)
                if custid and agentid:
                    qs = qs.filter(
                        Q(productionid__custid_id=custid)
                        | Q(productionid__agentid_id=agentid)
                    )
                elif custid:
                    qs = qs.filter(productionid__custid_id=custid)
                elif agentid:
                    qs = qs.filter(productionid__agentid_id=agentid)
        return qs.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listdata"] = list(context["object_list"])
        base_url = reverse("invoice:TProductionReel_list")
        params = []
        production_id = self.request.GET.get("production")
        custid = self.request.GET.get("custid")
        agentid = self.request.GET.get("agentid")
        if production_id:
            params.append(f"production={production_id}")
        if custid:
            params.append(f"custid={custid}")
        if agentid:
            params.append(f"agentid={agentid}")
        context["modelurl"] = f"{base_url}?{'&'.join(params)}" if params else base_url
        context["reelview_id"] = "reelview"
        return context

class ProductionApproval(SuccessMessageMixin, FormView):
    """Filter form for Production Approval (reuses TProduction-style rdate). Table shows non-approved only."""
    form_class = mf.ProductionApprovalFilterForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:ProductionApproval_list")

    def get_context_data(self, *args, **kwargs):
        base_list_url = reverse("invoice:ProductionApproval_list")
        select_all_js = (
            "document.querySelectorAll('#table-body input[name=selected_row]').forEach("
            "function(c){ c.checked = true; }); return false;"
        )
        btn = {
            "buttons": {
                "select_all": {
                    "type": "button",
                    "value": "Select all",
                    "attrs": {"onclick": select_all_js},
                },
                "Find": {
                    "type": "button",
                    "value": "Find",
                    "hx_req_type": "hx-get",
                    "hx_req": base_list_url,
                    "hx_target": "#tableview-tableshow",
                    "hx_swap": "outerHTML",
                    "attrs": {"hx-include": "closest form"},
                },
                "Approve": {
                    "type": "button",
                    "value": "Approve",
                    "hx_req_type": "hx-post",
                    "hx_req": reverse("invoice:ProductionApproval_approve"),
                    "hx_target": "#tableview-tableshow",
                    "hx_swap": "outerHTML",
                    "attrs": {"hx-include": "[name='selected_row']:checked, [name=rdate]"},
                },
            }
        }
        context = super().get_context_data(*args, **kwargs)
        context["buttons"] = hf.btn_append(btn,"buttons")
        return context

class ProductionApproval_list(ListView):
    """Table of TProduction entries that are not approved; optional filter by rdate."""
    model = TProduction
    exclude = ["productionid", "apiflag", "fac", "stk",
               "entrytype", "headid", "ind_weight",
               "obflag", "refproductionid"]
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        qs = TProduction.objects.exclude(approved=True).annotate(
            pk_str=Cast("pk", output_field=CharField())
        )
        rdate = self.request.GET.get("rdate")
        if rdate:
            qs = qs.filter(rdate=rdate)
        return qs.select_related(
            "agentid", "custid", "category", "itemcode", "shadecode"
        ).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listdata"] = list(context["object_list"])
        base_url = reverse("invoice:ProductionApproval_list")
        rdate = self.request.GET.get("rdate")
        if rdate:
            context["modelurl"] = f"{base_url}?rdate={rdate}"
        else:
            context["modelurl"] = base_url
        return context

class ProductionApproval_approve(View):
    """POST with selected_row: set approved=True on those TProduction records and re-render table."""

    def post(self, request, *args, **kwargs):
        selected = request.POST.getlist("selected_row")
        if selected:
            TProduction.objects.filter(pk__in=selected).update(approved=True,stk=True)
            messages.success(request, "Production entries approved.")
        rdate = request.POST.get("rdate")
        if not rdate and request.META.get("HTTP_REFERER"):
            query = parse_qs(urlparse(request.META["HTTP_REFERER"]).query)
            rdate = (query.get("rdate") or [None])[0]
        # Re-render the list table with same filters by dispatching a GET to the list view
        return HttpResponseRedirect(reverse_lazy("invoice:ProductionApproval_list", kwargs={"rdate": rdate} if rdate else {}))