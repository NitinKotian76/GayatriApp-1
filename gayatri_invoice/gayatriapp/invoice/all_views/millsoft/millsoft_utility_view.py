import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.template import context
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from ...form_files.helperFunct import button
from ...form_files import millsoftForm as mf
logger = logging.getLogger(__name__)


class StockTransfer(SuccessMessageMixin, FormView):
    """
    for transferring stock from one agent/customer/excessStocklot to another 
    """
    form_class = mf.StockTransferForm
    context_object_name = "form"
    success_url = reverse_lazy("invoice:StockTransfer")
    success_message = "successfully transferred"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["buttons"] = button(
            "submit",
            hx_req_type="hx-post",
            hx_req=reverse_lazy("invoice:StockTransfer"),
            hx_target="#dynform",
            hx_swap="innerHTML")
        return context

    # def form_valid(self, form):
    #     # save the production record
    #     return super().form_valid(form)


class MAgentAutocomplete():
    pass


def ApiView(request):
    pass
