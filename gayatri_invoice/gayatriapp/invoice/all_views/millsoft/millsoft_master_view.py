
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView, DeleteView, ListView)
from django.urls import (reverse_lazy, reverse)
from django_htmx.http import trigger_client_event
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db.models.functions import Cast
from django.db.models import CharField

from ...form_files import (helperFunct as hf, millsoftForm as mf)
from ...models import (MAgent, MUnit, MCustomer,
                       MExportFields, MItem, MItemCategory,
                       MLocation, MPlusMinusHead, MShade)
from .services import (_set_initial_values_from_form_data, _itemcode_from_shadeid)
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
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=reverse('invoice:MAgent_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MAgent_update(SuccessMessageMixin, UpdateView):
    model = MAgent
    form_class = mf.MAgentForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MAgent_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


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
        return MAgent.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context["modelurl"] = reverse('invoice:MAgent_list')
        return context


class MUnit_create(SuccessMessageMixin, CreateView):
    model = MUnit
    form_class = mf.MUnitForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MUnit_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=reverse('invoice:MUnit_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")

class MUnit_update(SuccessMessageMixin, UpdateView):
    model = MUnit
    form_class = mf.MUnitForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MUnit_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")

class MUnit_delete(SuccessMessageMixin, DeleteView):
    model = MUnit
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MUnit_list')

@method_decorator(never_cache, name='dispatch')
class MUnit_list(SuccessMessageMixin, ListView):
    model = MUnit
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MUnit.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = []
        context["modelurl"] = reverse('invoice:MUnit_list')
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
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=reverse(
                                           'invoice:MCustomer_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MCustomer_update(SuccessMessageMixin, UpdateView):

    model = MCustomer
    form_class = mf.MCustomerForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MCustomer_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MCustomer_delete(SuccessMessageMixin, DeleteView):

    model = MCustomer
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MCustomer_list')


@method_decorator(never_cache, name='dispatch')
class MCustomer_list(SuccessMessageMixin, ListView):

    model = MCustomer
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MCustomer.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context['buttons'] = []
        context["modelurl"] = reverse('invoice:MCustomer_list')
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
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=reverse(
                                           'invoice:MExportFields_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MExportFields_update(SuccessMessageMixin, UpdateView):

    model = MExportFields
    form_class = mf.MExportFieldsForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MExportFields_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MExportFields_delete(SuccessMessageMixin, DeleteView):

    model = MExportFields
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MExportFields_list')


@method_decorator(never_cache, name='dispatch')
class MExportFields_list(SuccessMessageMixin, ListView):

    model = MExportFields
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MExportFields.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context["modelurl"] = reverse('invoice:MExportFields_list')
        return context


class MItem_create(SuccessMessageMixin, CreateView):

    model = MItem
    form_class = mf.MItemForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MItem_create")
    success_message = "successfully created"

    def get_initial(self):

        initial = super().get_initial()
        if self.request.htmx and self.request.GET:
            form_data = self.request.GET
            initial = _set_initial_values_from_form_data(initial, form_data)
            initial = _itemcode_from_shadeid(initial)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=reverse('invoice:MItem_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MItem_update(SuccessMessageMixin, UpdateView):

    model = MItem
    form_class = mf.MItemForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MItem_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MItem_delete(SuccessMessageMixin, DeleteView):

    model = MItem
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MItem_list')


@method_decorator(never_cache, name='dispatch')
class MItem_list(SuccessMessageMixin, ListView):

    model = MItem
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MItem.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context["modelurl"] = reverse('invoice:MItem_list')
        return context


class MItemCategory_create(SuccessMessageMixin, CreateView):

    model = MItemCategory
    form_class = mf.MItemCategoryForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_url = reverse_lazy("invoice:MItemCategory_create")
    success_message = "successfully created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=reverse('invoice:MItemCategory_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MItemCategory_update(SuccessMessageMixin, UpdateView):

    model = MItemCategory
    form_class = mf.MItemCategoryForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MItemCategory_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MItemCategory_delete(SuccessMessageMixin, DeleteView):

    model = MItemCategory
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MItemCategory_list')


@method_decorator(never_cache, name='dispatch')
class MItemCategory_list(SuccessMessageMixin, ListView):

    model = MItemCategory
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MItemCategory.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context["modelurl"] = reverse('invoice:MItemCategory_list')
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
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=reverse(
                                           'invoice:MLocation_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MLocation_update(SuccessMessageMixin, UpdateView):

    model = MLocation
    form_class = mf.MLocationForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MLocation_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MLocation_delete(SuccessMessageMixin, DeleteView):

    model = MLocation
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MLocation_list')


@method_decorator(never_cache, name='dispatch')
class MLocation_list(SuccessMessageMixin, ListView):

    model = MLocation
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MLocation.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
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
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=reverse(
                                           'invoice:MPlusMinusHead_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MPlusMinusHead_update(SuccessMessageMixin, UpdateView):

    model = MPlusMinusHead
    form_class = mf.MPlusMinusHeadForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MPlusMinusHead_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MPlusMinusHead_delete(SuccessMessageMixin, DeleteView):

    model = MPlusMinusHead
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MPlusMinusHead_list')


@method_decorator(never_cache, name='dispatch')
class MPlusMinusHead_list(SuccessMessageMixin, ListView):

    model = MPlusMinusHead
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MPlusMinusHead.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
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
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=reverse('invoice:MShade_create'),
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")
        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MShade_update(SuccessMessageMixin, UpdateView):

    model = MShade
    form_class = mf.MShadeForm
    template_name = "partials/forms.html"
    context_object_name = "form"
    success_message = "successfully updated"
    success_url = reverse_lazy('invoice:MShade_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buttons"] = hf.button(type="submit", value="submit",
                                       hx_req=f"{self.request.path}",
                                       hx_target="#dynform",
                                       hx_swap="innerHTML")

        return context

    def form_valid(self, form):
        form.save()
        response = self.render_to_response(self.get_context_data())
        return trigger_client_event(response, "RefreshTable", after="settle")


class MShade_delete(SuccessMessageMixin, DeleteView):

    model = MShade
    success_message = "successfully deleted"
    success_url = reverse_lazy('invoice:MShade_list')


@method_decorator(never_cache, name='dispatch')
class MShade_list(SuccessMessageMixin, ListView):

    model = MShade
    fields = '__all__'
    context_object_name = "form"
    template_name = "partials/tableview.html"
    paginate_by = 100

    def get_queryset(self):
        return MShade.objects.annotate(pk_str=Cast("pk", output_field=CharField())).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Already dicts from .values()
        context['listdata'] = list(context['object_list'])
        context["modelurl"] = reverse('invoice:MShade_list')
        return context
