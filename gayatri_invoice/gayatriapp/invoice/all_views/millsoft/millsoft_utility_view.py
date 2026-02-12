import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.template import context
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from ...models import TProduction

from ...form_files.helperFunct import btn_append, button
from ...form_files import millsoftForm as mf
logger = logging.getLogger(__name__)


class StockTransfer(SuccessMessageMixin, FormView):
    """
    for transferring stock from one agent/customer/excessStocklot to another 
    """
    form_class = mf.StockTransferForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:StockTransfer")
    success_message = "successfully transferred"

    def get_context_data(self, *args, **kwargs):
        btn = {
            "buttons": {
                "transfer": {
                    "hx_req_type": "hx-post",
                    "hx_req": reverse_lazy("invoice:StockTransfer"),
                    "hx_target": "#dynform",
                    "hx_swap": "innerHTML",
                    "attrs": {"hx-include": "[input[name=selected_rows]]"}
                },
                "find": {
                    "hx_req_type": "hx-get",
                    "hx_req": reverse_lazy("invoice:TProduction_list"),
                    "hx_target": "#tableshow",
                    "hx_swap": "innerHTML",
                    "attrs": {"hx-include": "input#filter"}
                },
            }
        }
        context = super().get_context_data(*args, **kwargs)
        context["buttons"] = btn_append(btn, "buttons")

        return context

    def form_valid(self, form):
        selected_rows = self.request.POST.getlist("selected_rows")
        customer = self.request.POST.get("customer")
        agent = self.request.POST.get("agent")

        ids = [pk for pk in selected_rows]
        records = TProduction.objects.filter(pk__in=ids)
        logger.debug(records.values('pk'))
        TProduction.objects.bulk_update(records, [customer, agent])

        return trigger_client_event(self.request, "RefreshTable")


def ApiView(request):
    pass
