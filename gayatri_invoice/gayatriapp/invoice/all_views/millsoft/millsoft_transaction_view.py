from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DeleteView, ListView)
from django.urls import (reverse_lazy, reverse)
from django_htmx.http import trigger_client_event
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from ...form_files import (helperFunct as hf, millsoftForm as mf)
from ...models import (TempDP, TempWeightSlip, TExport, TExportDetails, TIndent,
                       TInvoice, TJumboRollWiseQC, TLOTNoWiseQc, TProduction,
                       TProduction_bck, TProductionReel, TWB)
import logging
logger = logging.getLogger(__name__)


class TempDP_create(SuccessMessageMixin, CreateView):

    model = TempDP
    form_class = mf.TempDPForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TempDP_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse('invoice:TempDP_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TempDP_update(SuccessMessageMixin, UpdateView):

    model = TempDP
    form_class = mf.TempDPForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TempDP_create')

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
        return trigger_client_event(response, "RefreshTable")


class TempDP_delete(SuccessMessageMixin, DeleteView):

    model = TempDP
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TempDP_list')


class TempDP_list(SuccessMessageMixin, ListView):

    model = TempDP
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TempDP.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TempDP_list')
        return context


class TempWeightSlip_create(SuccessMessageMixin, CreateView):

    model = TempWeightSlip
    form_class = mf.TempWeightSlipForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TempWeightSlip_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:TempWeightSlip_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TempWeightSlip_update(SuccessMessageMixin, UpdateView):

    model = TempWeightSlip
    form_class = mf.TempWeightSlipForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TempWeightSlip_create')

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
        return trigger_client_event(response, "RefreshTable")


class TempWeightSlip_delete(SuccessMessageMixin, DeleteView):

    model = TempWeightSlip
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TempWeightSlip_list')


class TempWeightSlip_list(SuccessMessageMixin, ListView):

    model = TempWeightSlip
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TempWeightSlip.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TempWeightSlip_list')
        return context


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
        return trigger_client_event(response, "RefreshTable")


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
        return trigger_client_event(response, "RefreshTable")


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
        return TExport.objects.values()

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
        return trigger_client_event(response, "RefreshTable")


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
        return trigger_client_event(response, "RefreshTable")


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
        return TExportDetails.objects.values()

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


class TIndent_create(SuccessMessageMixin, CreateView):

    model = TIndent
    form_class = mf.TIndentForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TIndent_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:TIndent_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TIndent_update(SuccessMessageMixin, UpdateView):

    model = TIndent
    form_class = mf.TIndentForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TIndent_create')

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
        return trigger_client_event(response, "RefreshTable")


class TIndent_delete(SuccessMessageMixin, DeleteView):

    model = TIndent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TIndent_list')


class TIndent_list(SuccessMessageMixin, ListView):

    model = TIndent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TIndent.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TIndent_list')
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
                "submit": {
                    "hx_req": reverse('invoice:TInvoice_create'),
                    "hx_target": "#dynform",
                    "hx_swap": "innerHTML"
                },
                "submit": {
                    "hx_req": reverse('invoice:TInvoice_create'),
                    "hx_target": "#dynform",
                    "hx_swap": "innerHTML"
                }
            }
        )
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


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
        return trigger_client_event(response, "RefreshTable")


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
        return TInvoice.objects.values()

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


class TJumboRollWiseQC_create(SuccessMessageMixin, CreateView):

    model = TJumboRollWiseQC
    form_class = mf.TJumboRollWiseQCForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TJumboRollWiseQC_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:TJumboRollWiseQC_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TJumboRollWiseQC_update(SuccessMessageMixin, UpdateView):

    model = TJumboRollWiseQC
    form_class = mf.TJumboRollWiseQCForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TJumboRollWiseQC_create')

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
        return trigger_client_event(response, "RefreshTable")


class TJumboRollWiseQC_delete(SuccessMessageMixin, DeleteView):

    model = TJumboRollWiseQC
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TJumboRollWiseQC_list')


class TJumboRollWiseQC_list(SuccessMessageMixin, ListView):

    model = TJumboRollWiseQC
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TJumboRollWiseQC.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TJumboRollWiseQC_list')
        return context


class TLOTNoWiseQc_create(SuccessMessageMixin, CreateView):

    model = TLOTNoWiseQc
    form_class = mf.TLOTNoWiseQcForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TLOTNoWiseQc_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:TLOTNoWiseQc_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TLOTNoWiseQc_update(SuccessMessageMixin, UpdateView):

    model = TLOTNoWiseQc
    form_class = mf.TLOTNoWiseQcForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TLOTNoWiseQc_create')

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
        return trigger_client_event(response, "RefreshTable")


class TLOTNoWiseQc_delete(SuccessMessageMixin, DeleteView):

    model = TLOTNoWiseQc
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TLOTNoWiseQc_list')


class TLOTNoWiseQc_list(SuccessMessageMixin, ListView):

    model = TLOTNoWiseQc
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TLOTNoWiseQc.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TLOTNoWiseQc_list')
        return context


class TProduction_create(SuccessMessageMixin, CreateView):

    model = TProduction
    form_class = mf.TProductionForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TProduction_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:TProduction_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TProduction_update(SuccessMessageMixin, UpdateView):

    model = TProduction
    form_class = mf.TProductionForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TProduction_create')

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
        return trigger_client_event(response, "RefreshTable")


class TProduction_delete(SuccessMessageMixin, DeleteView):

    model = TProduction
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TProduction_list')


class TProduction_list(SuccessMessageMixin, ListView):

    model = TProduction
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TProduction.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create ", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TProduction_list')
        return context


class TProduction_bck_create(SuccessMessageMixin, CreateView):

    model = TProduction_bck
    form_class = mf.TProduction_bckForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TProduction_bck_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:TProduction_bck_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TProduction_bck_update(SuccessMessageMixin, UpdateView):

    model = TProduction_bck
    form_class = mf.TProduction_bckForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TProduction_bck_create')

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
        return trigger_client_event(response, "RefreshTable")


class TProduction_bck_delete(SuccessMessageMixin, DeleteView):

    model = TProduction_bck
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TProduction_bck_list')


class TProduction_bck_list(SuccessMessageMixin, ListView):

    model = TProduction_bck
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TProduction_bck.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TProduction_bck_list')
        return context


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
        return trigger_client_event(response, "RefreshTable")


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
        return trigger_client_event(response, "RefreshTable")


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
        return TProductionReel.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TProductionReel_list')
        return context


class TWB_create(SuccessMessageMixin, CreateView):

    model = TWB
    form_class = mf.TWBForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:TWB_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse('invoice:TWB_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TWB_update(SuccessMessageMixin, UpdateView):

    model = TWB
    form_class = mf.TWBForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:TWB_create')

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
        return trigger_client_event(response, "RefreshTable")


class TWB_delete(SuccessMessageMixin, DeleteView):

    model = TWB
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:TWB_list')


class TWB_list(SuccessMessageMixin, ListView):

    model = TWB
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return TWB.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:TWB_list')
        return context
