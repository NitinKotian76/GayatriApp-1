from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.http import HttpResponse

from ...models import TProduction
from ...form_files import helperFunct as hf, millsoftForm as mf
from ...form_files.helperFunct import btn_append
from django.contrib import messages
from django_htmx.http import trigger_client_event

import logging
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
                    "type": "submit",
                    "value": "transfer",
                    "hx_req_type": "hx-post",
                    "hx_req": reverse_lazy("invoice:StockTransfer"),
                    "hx_target": "#dynform",
                    "hx_swap": "innerHTML",
                    "attrs": {
                        "hx-include": "[name='selected_row']:checked"
                    }
                },
                "find": {
                    "type": "button",
                    "value": "find",
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
        logger.debug("form method called")
        selected_rows = self.request.POST.getlist("selected_row")
        logger.debug(selected_rows)
        customer = form.cleaned_data.get("party")
        agent = form.cleaned_data.get("agent")

        records = list(TProduction.objects.filter(pk__in=selected_rows))
        logger.debug(f"Records:{records}")

        for r in records:
            if customer:
                r.custid_id = customer
            if agent:
                r.agentid_id = agent

        result = TProduction.objects.bulk_update(
            records, ["custid", "agentid"])
        logger.debug(f"updated {result}")
        messages.success(self.request, self.success_message)
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTableview", after="settle")

    def form_invalid(self, form):
        logger.debug("form_invalid called")
        logger.debug("form.errors: %s", form.errors.as_data())
        logger.debug("form.non_field_errors: %s", form.non_field_errors())
        return super().form_invalid(form)


def ApiView(request):
    pass