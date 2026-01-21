from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DeleteView, ListView)
from django.urls import (reverse_lazy, reverse)
from django_htmx.http import trigger_client_event
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from ..form_files import (helperFunct as hf, millsoftForm as mf)
from ..models import (TempDP, TempWeightSlip, TExport, TExportDetails, TIndent,
                      TInvoice, TJumboRollWiseQC, TLOTNoWiseQc, TProduction,
                      TProduction_bck, TProductionReel, TWB)
import logging
logger = logging.getLogger(__name__)


class TempDP_create(SuccessMessageMixin, CreateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TempDP_update(SuccessMessageMixin, UpdateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TempDP_delete(SuccessMessageMixin, DeleteView):

    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


class TempDP_list(SuccessMessageMixin, ListView):

    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values()

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


class TempWeightSlip_create(SuccessMessageMixin, CreateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TempWeightSlip_update(SuccessMessageMixin, UpdateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TempWeightSlip_delete(SuccessMessageMixin, DeleteView):

    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


class TempWeightSlip_list(SuccessMessageMixin, ListView):

    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values()

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


class TExport_create(SuccessMessageMixin, CreateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TExport_update(SuccessMessageMixin, UpdateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TExport_delete(SuccessMessageMixin, DeleteView):

    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


class TExport_list(SuccessMessageMixin, ListView):

    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values()

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


class TExportDetails_create(SuccessMessageMixin, CreateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TExportDetails_update(SuccessMessageMixin, UpdateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TExportDetails_delete(SuccessMessageMixin, DeleteView):

    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


class TExportDetails_list(SuccessMessageMixin, ListView):

    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values()

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


class TIndent_create(SuccessMessageMixin, CreateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TIndent_update(SuccessMessageMixin, UpdateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TIndent_delete(SuccessMessageMixin, DeleteView):

    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


class TIndent_list(SuccessMessageMixin, ListView):

    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values()

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


class TInvoice_create(SuccessMessageMixin, CreateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TInvoice_update(SuccessMessageMixin, UpdateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TInvoice_delete(SuccessMessageMixin, DeleteView):

    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


class TInvoice_list(SuccessMessageMixin, ListView):

    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values()

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


class TJumboRollWiseQC_create(SuccessMessageMixin, CreateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TJumboRollWiseQC_update(SuccessMessageMixin, UpdateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TJumboRollWiseQC_delete(SuccessMessageMixin, DeleteView):

    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


class TJumboRollWiseQC_list(SuccessMessageMixin, ListView):

    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values()

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


class TLOTNoWiseQc_create(SuccessMessageMixin, CreateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TLOTNoWiseQc_update(SuccessMessageMixin, UpdateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TLOTNoWiseQc_delete(SuccessMessageMixin, DeleteView):

    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


class TLOTNoWiseQc_list(SuccessMessageMixin, ListView):

    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values()

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


class TProduction_create(SuccessMessageMixin, CreateView):

    model = TProduction
    form_class = mf.TProductionForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MAgent_create")
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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TProduction_bck_update(SuccessMessageMixin, UpdateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TProduction_bck_delete(SuccessMessageMixin, DeleteView):

    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


class TProduction_bck_list(SuccessMessageMixin, ListView):

    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values()

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


class TProductionReel_create(SuccessMessageMixin, CreateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TProductionReel_update(SuccessMessageMixin, UpdateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TProductionReel_delete(SuccessMessageMixin, DeleteView):

    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


class TProductionReel_list(SuccessMessageMixin, ListView):

    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values()

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


class TWB_create(SuccessMessageMixin, CreateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TWB_update(SuccessMessageMixin, UpdateView):

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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class TWB_delete(SuccessMessageMixin, DeleteView):

    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


class TWB_list(SuccessMessageMixin, ListView):

    model = MAgent
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MAgent.objects.values()

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
