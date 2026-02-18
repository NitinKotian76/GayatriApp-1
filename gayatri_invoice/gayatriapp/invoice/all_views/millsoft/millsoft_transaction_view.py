from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DeleteView, ListView, FormView)
from django.urls import (reverse_lazy, reverse)
from django_htmx.http import trigger_client_event
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db.models.functions import Cast
from django.db.models import CharField
from django.db.models import Q, F
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages


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
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:TExport_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
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
        context["buttons"] = hf.button("submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

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
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:TExportDetails_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
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
        context["buttons"] = hf.button("submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

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
        context["buttons"] = hf.btn_append(
            {
                "buttons": {
                    "submit": {
                        "hx_req": reverse('invoice:TInvoice_create'),
                        "hx_target": "#dynform",
                        "hx_swap": "innerHTML"
                    },
                    "challan": {
                        "hx_req": reverse('invoice:RChallan_create'),
                        "hx_swap": "none",
                    },
                    "gate_pass": {
                        "hx_req": reverse('invoice:GatePass_create'),
                        "hx_swap": "none",
                    },
                    "invoice": {
                        "hx_req": reverse('invoice:Invoice_create'),
                        "hx_swap": "none",
                    }
                }
            },
            "buttons"
        )
        return context

    def form_valid(self, form):
        form.save()
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
        context["buttons"] = hf.button("submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")


class TInvoice_delete(SuccessMessageMixin, DeleteView):

    model = TInvoice
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TInvoice_list')


@method_decorator(never_cache, name='dispatch')
class TInvoice_list(SuccessMessageMixin, ListView):

    model = TInvoice
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TInvoice.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
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
                # size(cm) * gsm(gm) * length(cm) / 10000000000 * noofsheet (sheets)
                form_data["reamwt"] = str(int(float(size) * float(gsm) * float(length) /1000000)* int(noofsheet))
            except (ValueError, TypeError):
                pass

        if reamwt and noofream:
            try:
                form_data["weight"] = str(int(reamwt) * int(noofream))
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
                    "submit",
                    hx_req=reverse("invoice:TProduction_create"),
                    hx_target="#dynform",
                    hx_swap="innerHTML",
                ),
                "reel_numbers": reel_numbers,
                "reel_total": reel_total,
            }
            form_html = render_to_string(self.template_name, context, request=request)
            preview_html = render_to_string(
                "partials/reel_preview.html",
                {"reel_numbers": reel_numbers, "reel_total": reel_total},
                request=request,
            )
            return HttpResponse(form_html + preview_html)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:TProduction_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML",
                                       hx_confirm="Are you sure you want to create these reels?")
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



# class TProduction_update(SuccessMessageMixin, UpdateView):

#     model = TProduction
#     form_class = mf.TProductionForm
#     template_name = "partials/forms.html"
#     context_object_name = "form"
#     success_message = "successfully updated"
#     success_url = reverse_lazy('invoice:TProduction_create')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["buttons"] = hf.button("submit",
#                                        hx_req=f"{self.request.path}",
#                                        hx_target="#dynform",
#                                        hx_swap="innerHTML")

#         return context

#     def form_valid(self, form):
#         form.save()
#         response = self.render_to_response(self.get_context_data())
#         return trigger_client_event(response, "RefreshTableview", after="settle")


class TProduction_delete(SuccessMessageMixin, DeleteView):

    model = TProduction
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TProduction_list')


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
        context['buttons'] = [
            hf.button("Create ", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TProduction_list')
        context['show_reel_button'] = True
        return context

class TStockplusminus(SuccessMessageMixin, UpdateView):

    model = TProduction
    form_class = mf.TStockplusminusForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TStockplusminus')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

        return context

    def form_valid(self, form):
        form.save()
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
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:TProductionReel_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
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
        context["buttons"] = hf.button("submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

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
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        qs = TProductionReel.objects.annotate(
            pk_str=Cast("pk", output_field=CharField())
        )
        production_id = self.request.GET.get('production')
        if production_id:
            qs = qs.filter(productionid_id=production_id)
        return qs.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        base_url = reverse('invoice:TProductionReel_list')
        production_id = self.request.GET.get('production')
        if production_id:
            context["modelurl"] = f"{base_url}?production={production_id}"
        else:
            context["modelurl"] = base_url
        return context
