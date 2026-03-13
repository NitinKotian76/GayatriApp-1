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
    _set_selected_reels_and_productions_out_of_stock,
    _get_reel_numbers,
    _autocomplete_form_data,
    _get_productionreel_list_data,
    _set_initial_values_from_form_data,
    _agentid_from_custid,
    _data_for_reel_preview,
)
from ...form_files import (helperFunct as hf, millsoftForm as mf)
from ...models import (TExport, TExportDetails,
                       TInvoice, TProduction,
                       TProductionReel, MItem, MCustomer)
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
                                       hx_target="#form-column",
                                       hx_swap="innerHTML",
                                       )
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")


@method_decorator(never_cache, name='dispatch')
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
                                       hx_target="#form-column",
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
                                       hx_target="#form-column",
                                       hx_swap="innerHTML",
                                       )
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

@method_decorator(never_cache, name='dispatch')
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
                                       hx_target="#form-column",
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


class TProduction_create(SuccessMessageMixin, CreateView):

    model = TProduction
    form_class = mf.TProductionForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TProduction_create")
    success_message = "successfully created"

    # this is only used for reel preview
    def get_initial(self):
        initial = super().get_initial()
        if self.request.htmx and self.request.GET:
            form_data = self.request.GET
            initial = _set_initial_values_from_form_data(initial, form_data) # gets the user input from form_data and sets it to initial
            initial= _agentid_from_custid(initial) # gets the agentid from the custid
            initial = _autocomplete_form_data(initial) # gets the autocomplete data using initial
        return initial

    def get(self, request, *args, **kwargs):
        response=super().get(request, *args, **kwargs)
        if self.request.htmx:
            if hasattr(response, "render"):
                response.render()
            response = trigger_client_event(response, "RefreshReelPreview", after="settle")
        return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        btn = {
            "buttons": {
                "submit": {
                    "type": "submit",
                    "value": "submit",
                    "hx_req": f"{self.request.path}",
                    "hx_target": "#form-column",
                    "hx_swap": "outerHTML",
                },
                "formula": {
                    "type": "checkbox",
                    "value": "formula",
                    "attrs":{"id":"formula"},
                }
            }
        }
        context["buttons"] = hf.btn_append(btn, "buttons")
        return context

    def form_valid(self, form):
        production = form.save(commit=False)
        # reamwt is the ind_weight (individual weight of the bundle)
        if production.reamwt is not None:
            production.ind_weight = production.reamwt
        production.stk = True
        production.save()
        form.save_m2m()
        excise_from = production.excise_from or 0
        excise_to = production.excise_to or excise_from
        for reelno in range(int(excise_from), int(excise_to) + 1):
            TProductionReel.objects.create(
                productionid=production,
                reelno=reelno,
                stkdate=production.rdate,
                stk="true",
            )
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")
    
@method_decorator(never_cache, name='dispatch')
class TProduction_update(SuccessMessageMixin, UpdateView):

    model = TProduction
    form_class = mf.TProductionForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TProduction_create')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["htmx_get_url"] = self.request.path
        return kwargs
    # this is only used for reel preview
    def get_initial(self):
        initial = super().get_initial()
        if self.request.htmx and self.request.GET:
            form_data = self.request.GET
            initial = _set_initial_values_from_form_data(initial, form_data) # gets the user input from form_data and sets it to initial
            initial= _agentid_from_custid(initial) # gets the agentid from the custid
            initial = _autocomplete_form_data(initial) # gets the autocomplete data using initial
        return initial

    def get(self, request, *args, **kwargs):
        response=super().get(request, *args, **kwargs)
        if self.request.htmx:
            if hasattr(response, "render"):
                response.render()
            response = trigger_client_event(response, "RefreshReelPreview", after="settle")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        btn = {
            "buttons": {
                "submit": {
                    "type": "submit",
                    "value": "submit",
                    "hx_req": f"{self.request.path}",
                    "hx_target": "#form-column",
                    "hx_swap": "outerHTML",
                },
                "formula": {
                    "type": "checkbox",
                    "value": "formula",
                    "attrs":{"id":"formula"},
                }
            }
        }
        context["buttons"] = hf.btn_append(btn, "buttons")
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
    exclude = ["productionid", "apiflag", "fsc", "stk", 
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


class TInvoice_create(SuccessMessageMixin, CreateView):

    model = TInvoice
    form_class = mf.TInvoiceForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TInvoice_create")
    success_message = "successfully created"

    def get_initial(self):
        initial = super().get_initial()
        if self.request.htmx and self.request.GET:
            form_data = self.request.GET
            initial = _set_initial_values_from_form_data(initial, form_data)
            initial= _agentid_from_custid(initial)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        btn = { 
            "buttons": {
                "select_all": {
                    "type": "button",
                    "value": "Select all",
                    "attrs": {"onclick": "selectAll()"},
                },
                "clear_selected_rows": {
                    "type": "button",
                    "value": "Clear selected rows",
                    "attrs": {"onclick": "clearSelectedRows()"},
                },
                "submit": {
                    "type": "submit",
                    "value": "submit",
                    "hx_req": reverse('invoice:TInvoice_create'),
                    "hx_target": "#form-column",
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
        selected_reel_ids = self.request.session.get("selected_rows") or []
        if selected_reel_ids:
            _set_selected_reels_and_productions_out_of_stock(form.instance, selected_reel_ids)
            self.request.session["selected_rows"] = []
            self.request.session.modified = True
        else:
            _set_invoice_productions_out_of_stock(form.instance)
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

@method_decorator(never_cache, name='dispatch')
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
            hf.button(type="submit", value="submit", hx_req=f"{self.request.path}", hx_target="#form-column", hx_swap="outerHTML"),
        ]

        return context

    def form_valid(self, form):
        form.save()
        selected_reel_ids = self.request.session.get("selected_rows") or []
        if selected_reel_ids:
            _set_selected_reels_and_productions_out_of_stock(form.instance, selected_reel_ids)
            self.request.session["selected_rows"] = []
            self.request.session.modified = True
        else:
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
    exclude = ["invoiceid", "apiflag", "fsc", "stk"] 
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
                                       hx_target="#form-column",
                                       hx_swap="outerHTML"),
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

@method_decorator(never_cache, name='dispatch')
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["htmx_get_url"] = self.request.path
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        if self.request.htmx and self.request.GET:
            form_data = self.request.GET
            initial = _set_initial_values_from_form_data(initial, form_data) # gets the user input from form_data and sets it to initial
            initial= _agentid_from_custid(initial) # gets the agentid from the custid
            initial = _autocomplete_form_data(initial) # gets the autocomplete data using initial
        return initial

    def get(self, request, *args, **kwargs):
        response=super().get(request, *args, **kwargs)
        if self.request.htmx:
            if hasattr(response, "render"):
                response.render()
            response = trigger_client_event(response, "RefreshReelPreview", after="settle")
        return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(
            type="submit", value="submit",
            hx_req=f"{self.request.path}",
            hx_target="#form-column",
            hx_swap="outerHTML"
        )
        return context

    def form_valid(self, form):
        original = self.object
        original_reels = TProductionReel.objects.filter(productionid=original)
        # Capture original PK before we mutate the instance (form instance is the same object as original)
        original_productionid = original.productionid
        # Create new TProduction from form, do not update the original
        new_production = form.save(commit=False)
        new_production.pk = None
        new_production.productionid = None
        new_production.refproductionid = original_productionid
        if new_production.reamwt is not None:
            new_production.ind_weight = new_production.reamwt
        new_production.stk = True
        original.stk = False
        original_reels.update(stk=False)
        original.save()
        new_production.save()
        form.save_m2m()
        # Create TProductionReel rows for the new production (match excise_from/excise_to)
        excise_from = new_production.excise_from or 0
        excise_to = new_production.excise_to or excise_from
        for reelno in range(int(excise_from), int(excise_to) + 1):
            new_reel = TProductionReel.objects.create(
                productionid=new_production,
                reelno=reelno,
                stkdate=new_production.rdate,
                stk="True",
            )
            new_reel.save()
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
                                       hx_target="#form-column",
                                       hx_swap="outerHTML"),
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshReelview", after="settle")

@method_decorator(never_cache, name='dispatch')
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
                                       hx_target="#form-column",
                                       hx_swap="outerHTML"),

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
    exclude = ["productionreelid", "apiflag", "fsc", "stk"]
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
        # Template uses /invoice/{{ modelurl }} for some links; pass path relative to /invoice/
        if base_url.startswith("/invoice/"):
            base_url = base_url[len("/invoice/"):]
        params = []
        production_id = self.request.GET.get("production")
        custid = self.request.GET.get("custid")
        agentid = self.request.GET.get("agentid")
        shadeid = self.request.GET.get("shadeid")
        if production_id:
            params.append(f"production={production_id}")
        if custid:
            params.append(f"custid={custid}")
        if agentid:
            params.append(f"agentid={agentid}")
        if shadeid:
            params.append(f"shadeid={shadeid}")
        context["modelurl"] = f"{base_url}?{'&'.join(params)}" if params else base_url
        context["modelurl_base"] = base_url
        context["reelview_id"] = "reelview"
        return context

class TInvoice_productionreel_list(TProductionReel_list):
    """List of production for the selected invoice."""
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.htmx and self.request.GET:
             qs = _get_productionreel_list_data(self.request.GET,qs)
        return qs

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self.request.htmx:
            if hasattr(response, "render"):
                response.render()
            response = trigger_client_event(response, "RefreshTableview", after="settle")
        return response


class ProductionApproval(SuccessMessageMixin, FormView):
    """Filter form for Production Approval (reuses TProduction-style rdate). Table shows non-approved only."""
    form_class = mf.ProductionApprovalFilterForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:ProductionApproval_list")

    def get_context_data(self, *args, **kwargs):
        base_list_url = reverse("invoice:ProductionApproval_list")
        btn = {
            "buttons": {
                "select_all": {
                    "type": "button",
                    "value": "Select all",
                    "attrs": {"onclick": "selectAll(); return false;"},
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