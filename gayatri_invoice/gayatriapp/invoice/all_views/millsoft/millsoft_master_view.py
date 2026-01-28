
from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DeleteView, ListView)
from django.urls import (reverse_lazy, reverse)
from django_htmx.http import trigger_client_event
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db.models.functions import Cast
from django.db.models import CharField

from ...form_files import (helperFunct as hf, millsoftForm as mf)
from ...models import (MAgent, MCategory, MCustomer, MEmployee,
                       MExportFields, MItem, MItemCategory, MItemRate,
                       MLocation, MPlusMinusHead, MShade, MSupplier)

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
        form.save()
        response = self.render_to_response(self.get_context_data())
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
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MAgent_delete(SuccessMessageMixin, DeleteView):
    model = MAgent
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MAgent_list')


@method_decorator(never_cache, name='dispatch')
class MAgent_list(ListView):
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


class MCategory_create(SuccessMessageMixin, CreateView):

    model = MCategory
    form_class = mf.MCategoryForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MCategory_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:MCategory_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MCategory_update(SuccessMessageMixin, UpdateView):

    model = MCategory
    form_class = mf.MCategoryForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MCategory_create')

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


class MCategory_delete(SuccessMessageMixin, DeleteView):

    model = MCategory
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MCategory_list')


class MCategory_list(SuccessMessageMixin, ListView):

    model = MCategory
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MCategory.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("button", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MCategory_list')
        return context


class MCustomer_create(SuccessMessageMixin, CreateView):

    model = MCustomer
    form_class = mf.MCustomerForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MCustomer_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:MCustomer_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MCustomer_update(SuccessMessageMixin, UpdateView):

    model = MCustomer
    form_class = mf.MCustomerForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MCustomer_create')

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


class MCustomer_delete(SuccessMessageMixin, DeleteView):

    model = MCustomer
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MCustomer_list')


class MCustomer_list(SuccessMessageMixin, ListView):

    model = MCustomer
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MCustomer.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MCustomer_list')
        return context


class MEmployee_create(SuccessMessageMixin, CreateView):

    model = MEmployee
    form_class = mf.MEmployeeForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MEmployee_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:MEmployee_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MEmployee_update(SuccessMessageMixin, UpdateView):

    model = MEmployee
    form_class = mf.MEmployeeForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MEmployee_create')

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


class MEmployee_delete(SuccessMessageMixin, DeleteView):

    model = MEmployee
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MEmployee_list')


class MEmployee_list(SuccessMessageMixin, ListView):

    model = MEmployee
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MEmployee.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MEmployee_list')
        return context


class MExportFields_create(SuccessMessageMixin, CreateView):

    model = MExportFields
    form_class = mf.MExportFieldsForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MExportFields_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:MExportFields_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MExportFields_update(SuccessMessageMixin, UpdateView):

    model = MExportFields
    form_class = mf.MExportFieldsForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MExportFields_create')

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


class MExportFields_delete(SuccessMessageMixin, DeleteView):

    model = MExportFields
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MExportFields_list')


class MExportFields_list(SuccessMessageMixin, ListView):

    model = MExportFields
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MExportFields.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MExportFields_list')
        return context


class MItem_create(SuccessMessageMixin, CreateView):

    model = MItem
    form_class = mf.MItemForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MItem_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse('invoice:MItem_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MItem_update(SuccessMessageMixin, UpdateView):

    model = MItem
    form_class = mf.MItemForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MItem_create')

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


class MItem_delete(SuccessMessageMixin, DeleteView):

    model = MItem
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MItem_list')


class MItem_list(SuccessMessageMixin, ListView):

    model = MItem
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MItem.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MItem_list')
        return context


class MItemCategory_create(SuccessMessageMixin, CreateView):

    model = MItem
    form_class = mf.MItemForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MItem_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse('invoice:MItem_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MItemCategory_update(SuccessMessageMixin, UpdateView):

    model = MItem
    form_class = mf.MItemForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MItem_create')

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


class MItemCategory_delete(SuccessMessageMixin, DeleteView):

    model = MItem
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MItem_list')


class MItemCategory_list(SuccessMessageMixin, ListView):

    model = MItem
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MItem.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MItem_list')
        return context


class MItemRate_create(SuccessMessageMixin, CreateView):

    model = MItemRate
    form_class = mf.MItemRateForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MItemRate_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:MItemRate_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MItemRate_update(SuccessMessageMixin, UpdateView):

    model = MItemRate
    form_class = mf.MItemRateForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MItemRate_create')

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


class MItemRate_delete(SuccessMessageMixin, DeleteView):

    model = MItemRate
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MItemRate_list')


class MItemRate_list(SuccessMessageMixin, ListView):

    model = MItemRate
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MItemRate.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MItemRate_list')
        return context


class MLocation_create(SuccessMessageMixin, CreateView):

    model = MLocation
    form_class = mf.MLocationForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MLocation_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:MLocation_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MLocation_update(SuccessMessageMixin, UpdateView):

    model = MLocation
    form_class = mf.MLocationForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MLocation_create')

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


class MLocation_delete(SuccessMessageMixin, DeleteView):

    model = MLocation
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MLocation_list')


class MLocation_list(SuccessMessageMixin, ListView):

    model = MLocation
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MLocation.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MLocation_list')
        return context


class MPlusMinusHead_create(SuccessMessageMixin, CreateView):

    model = MPlusMinusHead
    form_class = mf.MPlusMinusHeadForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MPlusMinusHead_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:MPlusMinusHead_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MPlusMinusHead_update(SuccessMessageMixin, UpdateView):

    model = MPlusMinusHead
    form_class = mf.MPlusMinusHeadForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MPlusMinusHead_create')

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


class MPlusMinusHead_delete(SuccessMessageMixin, DeleteView):

    model = MPlusMinusHead
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MPlusMinusHead_list')


class MPlusMinusHead_list(SuccessMessageMixin, ListView):

    model = MPlusMinusHead
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MPlusMinusHead.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MPlusMinusHead_list')
        return context


class MShade_create(SuccessMessageMixin, CreateView):

    model = MShade
    form_class = mf.MShadeForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MShade_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse('invoice:MShade_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MShade_update(SuccessMessageMixin, UpdateView):

    model = MShade
    form_class = mf.MShadeForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MShade_create')

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


class MShade_delete(SuccessMessageMixin, DeleteView):

    model = MShade
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MShade_list')


class MShade_list(SuccessMessageMixin, ListView):

    model = MShade
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MShade.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MShade_list')
        return context


class MSupplier_create(SuccessMessageMixin, CreateView):

    model = MSupplier
    form_class = mf.MSupplierForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MSupplier_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button("submit",
                                       hx_req=reverse(
                                           'invoice:MSupplier_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable")


class MSupplier_update(SuccessMessageMixin, UpdateView):

    model = MSupplier
    form_class = mf.MSupplierForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MSupplier_create')

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


class MSupplier_delete(SuccessMessageMixin, DeleteView):

    model = MSupplier
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MSupplier_list')


class MSupplier_list(SuccessMessageMixin, ListView):

    model = MSupplier
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MSupplier.objects.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = [
            hf.button("Create Agent", hx_req="",
                      hx_req_type="hx-get", hx_target="#tableshow")
        ]
        context["modelurl"] = reverse('invoice:MSupplier_list')
        return context
