from datetime import datetime
from ..models import (MAgent, MCategory, MCompany, MCustomer, MEmployee,
                      MExportFields, MItem, MItemCategory, MItemRate,
                      MLocation, MPlusMinusHead, MShade, MSupplier)
from ..models import (TempDP, TempWeightSlip, TExport, TExportDetails, TIndent,
                      TInvoice, TJumboRollWiseQC, TLOTNoWiseQc, TProduction,
                      TProduction_bck, TProductionReel, TWB)
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DeleteView, ListView)
from django.urls import (reverse_lazy, reverse)
from ..form_files import (helperFunct as hf, millsoftForm as mf)
from django_htmx.http import trigger_client_event
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
import logging
logger = logging.getLogger(__name__)


class MAgent_create(SuccessMessageMixin, CreateView):
    model = MAgent
    form_class = mf.MAgentForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MAgent_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse('invoice:MAgent_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return trigger_client_event(response, "RefreshTable")


class MAgent_update(SuccessMessageMixin, UpdateView):
    model = MAgent
    form_class = mf.MAgentForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MAgent_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return trigger_client_event(response, "RefreshTable")


class MAgent_delete(SuccessMessageMixin, DeleteView):
    model = MAgent
    form_class = mf.MAgentForm
    template_name = "form_snippet.html"
    context_object_name = "form"
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_create')


@method_decorator(never_cache, name='dispatch')
class MAgent_list(ListView):
    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values('id', 'AgentId', 'Agentname', 'Bname',
                                     'Area', 'City', 'Phone', 'Cell')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MAgent_list')
        return context

    # MCategory
    # MCompany
    # MCustomer
    # MEmployee
    # MExportFields
    # MItem
    # MItemCategory
    # MItemRate
    # MLocation
    # MPlusMinusHead
    # MShade
    # MSupplier
    # TempDP
    # TempWeightSlip
    # TExport
    # TExportDetails
    # TIndent
    # TInvoice
    # TJumboRollWiseQC
    # TLOTNoWiseQc
    # TProduction
    # TProduction_bck
    # TProductionReel
    # TWB
