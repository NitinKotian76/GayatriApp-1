from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DeleteView, ListView)
from django.urls import (reverse_lazy, reverse)
from django_htmx.http import trigger_client_event
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from ...form_files import (helperFunct as hf, millsoftForm as mf)
from ...models import (RChallan)

from weasyprint import HTML
import logging
logger = logging.getLogger(__name__)


class RChallan_create(SuccessMessageMixin, CreateView):
    model = RChallan
    success_url = reverse_lazy("invoice:RChallan_create")
    success_message = "successfully created"

    def form_valid(self, form):
        form.save()
        html_string = render_to_string(
            "DemoTemplate.html", {"company": "gayatrishakti paper and boards ltd"})
        HTML(html_string).write_pdf("demo.pdf")
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


# class RChallan_update(SuccessMessageMixin, UpdateView):
#     model = RChallan
#     form_class = mf.RChallanForm
#     template_name = "partials/forms.html"
#     context_object_name = "form"
#     success_message = "successfully updated"
#     success_url = reverse_lazy('invoice:RChallan_create')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["buttons"] = hf.button("submit",
#                                        hx_req=f"{self.request.path}",
#                                        hx_target="#dynform",
#                                        hx_swap="innerHTML")
#
#         return context
#
#     def form_valid(self, form):
#         form.save()
#         response = self.render_to_response(self.get_context_data())
#         return trigger_client_event(response, "RefreshTable")
#
#
# class RChallan_delete(SuccessMessageMixin, DeleteView):
#     model = RChallan
#     success_message = "successfully deleted"
#     success_url = reverse_lazy('invoice:RChallan_list')
#
#
# @method_decorator(never_cache, name='dispatch')
# class RChallan_list(ListView):
#     model = RChallan
#     fields = '__all__'
#     context_object_name = "form"
#     template_name = "partials/tableview.html"
#     paginate_by = 100
#
#     def get_queryset(self):
#         return RChallan.objects.values()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Already dicts from .values()
#         context['listdata'] = list(context['object_list'])
#         context['buttons'] = [
#             hf.button("Create Agent", hx_req="",
#                       hx_req_type="hx-get", hx_target="#tableshow")
#         ]
#         context["modelurl"] = reverse('invoice:RChallan_list')
#         return context
