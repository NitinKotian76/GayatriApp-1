from ..models import (MAgent, MCategory, MCustomer,
                      MExportFields, MItem, MItemCategory,
                      MLocation, MPlusMinusHead, MShade, MSupplier)
from ..models import (TExport, TExportDetails, TIndent,
                      TInvoice, TProduction,
                      TProduction_bck, TProductionReel)

from django.urls import (reverse_lazy, reverse)
from django import forms


class MAgentForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MAgent
        fields = "__all__"


class MCustomerForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MCustomer
        fields = "__all__"


class MCategoryForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MCategory
        fields = "__all__"


class MExportFieldsForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MExportFields
        fields = "__all__"


class MItemForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MItem
        fields = "__all__"


class MItemCategoryForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MItemCategory
        fields = "__all__"


class MLocationForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MLocation
        fields = "__all__"


class MPlusMinusHeadForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MPlusMinusHead
        fields = "__all__"


class MShadeForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MShade
        fields = "__all__"


class MSupplierForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MSupplier
        fields = "__all__"


class StockTransferForm(forms.Form):
    template_name = "form_snippet.html"

    party = forms.ChoiceField(
        choices=MCustomer.objects.all().values_list("pk", "custname"))
    agent = forms.ChoiceField(
        choices=MAgent.objects.all().values_list("pk", "agentname"))
    # search fields
    indentno = forms.CharField(
        widget=forms.TextInput(attrs={"id": "filter"}), required=False)
    # quality = forms.CharField(widget=forms.TextInput(attrs={"id": "filter"}))
    gsm = forms.CharField(widget=forms.TextInput(
        attrs={"id": "filter"}), required=False)
    sized = forms.CharField(widget=forms.TextInput(
        attrs={"id": "filter"}), required=False)
    length = forms.FloatField(widget=forms.TextInput(
        attrs={"id": "filter"}), required=False)
    rate = forms.FloatField(widget=forms.TextInput(
        attrs={"id": "filter"}), required=False)


class TExportForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TExport
        fields = "__all__"


class TExportDetailsForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TExportDetails
        fields = "__all__"



class TInvoiceForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TInvoice
        fields = "__all__"
        widgets = {
            "invoicedate": forms.DateInput(attrs={'type': 'date'}),
            "predate": forms.DateInput(attrs={'type': 'date'}),
            "remdate": forms.DateInput(attrs={'type': 'date'}),
            "lrdate": forms.DateInput(attrs={'type': 'date'}),
            "pretime": forms.TimeInput(attrs={'type': 'time'}),
            "remtime": forms.TimeInput(attrs={'type': 'time'}),
            # "AgentID":

        }


class TProductionForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TProduction
        fields = "__all__"
        widgets = {
            "rdate": forms.DateInput(attrs={'type': 'date'})
        }


class TProduction_bckForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TProduction_bck
        fields = "__all__"


class TProductionReelForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TProductionReel
        fields = "__all__"


class HTMXRelatedCompleteMixin:

    htmx_fields = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, config in self.htmx_fields.items():
            if field_name in self.fields:
                self.field[field_name].widget.attrs.update({
                    'hx-get': config['url'],
                    'hx-target': config['target'],
                    'hx-trigger': config['trigger'],
                    'hx-swap': 'outerHTML',
                })

        # get the relaton object m2m or 121
          # get the source field
          # get the target field
          # filter the target field qs by the field value in source field

        field_name = htmx_fields.keys()
        source = field_name[0]
        target = field_name[1]

        if self.data.get():
            sourcevalue = self.data.get(field_name)
        # if company var is not available put the first company name  or none
        if not company:
            first_company = Company.objects.first()
            company = first_company.id if not first_company else None
        # get the list of tablenames for the particular company
        self.fields[''].queryset
