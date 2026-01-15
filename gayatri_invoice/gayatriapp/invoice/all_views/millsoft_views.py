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
from django_htmx.http import retarget
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
        context["date"] = "hello"
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse('invoice:MAgent_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        context["update_url"] = 'MAgent_update'
        context["delete_url"] = 'MAgent_delete'

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class MAgent_update(SuccessMessageMixin, UpdateView):
    model = MAgent
    fields = ["AgentId", "Agentname", "Bname", "Area", "Road", "City", "Pin", "State",
              "Phone", "Cell", "range", "division"]
    template_name = "form_snippet.html"
    context_object_name = "form"
    success_message = "successfully updated %(Agentname)"
    success_url = reverse_lazy('invoice:MAgent_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse('invoice:MAgent_update'),)
        return context


class MAgent_delete(SuccessMessageMixin, DeleteView):
    model = MAgent
    fields = ["AgentId", "Agentname", "Bname", "Area", "Road", "City", "Pin", "State",
              "Phone", "Cell", "range", "division"]
    template_name = "form_snippet.html"
    context_object_name = "form"
    success_message = "successfully deleted %(Agentname)"
    success_url = reverse_lazy('invoice:MAgent_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req="/invoice/MAgent_delete",)
        return context


@method_decorator(never_cache, name='dispatch')
class MAgent_list(ListView):
    model = MAgent
    fields = ["AgentId", "Agentname", "Bname", "Area", "Road", "City", "Pin", "State",
              "Phone", "Cell", "range", "division"]
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
        return context


class MCategory(CreateView):
    pass
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
