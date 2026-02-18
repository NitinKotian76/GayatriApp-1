from ..models import (MAgent, MCustomer, MUnit,
                      MExportFields, MItem, MItemCategory,
                      MLocation, MPlusMinusHead, MShade)
from ..models import (TExport, TExportDetails,
                      TInvoice, TProduction, TProductionReel)
from django.urls import (reverse_lazy)
from django import forms


class MAgentForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MAgent
        fields = "__all__"
        widgets = {
            "invoicetype": forms.Select(choices=[(1, 'Tax Invoice'), (2, 'Retail Invoice')])

        }


class MCustomerForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MCustomer
        fields = "__all__"




class MExportFieldsForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MExportFields
        fields = "__all__"

class MUnitForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MUnit
        fields = "__all__"
        widgets = {
            "unit_type": forms.Select(choices=[(1, 'Weight'), (2, 'Length'), (3, 'Area'), (4, 'Volume'), (5, 'Time'), (6, 'Currency'), (7, 'Other')])
        }

class MItemForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MItem
        fields = "__all__"

class MShadeForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MShade
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
        widgets = {
            "plus_minus": forms.Select(choices=[('PLUS', 'Plus'), ('MINUS', 'Minus')]),
            "api": forms.Select(choices=[(True, 'True'), (False, 'False')]),
            "ref": forms.Select(choices=[('WITHREF', 'WITHREF'), ('WITHOUTREF', 'WITHOUTREF')]),
        }



class StockTransferForm(forms.Form):
    template_name = "form_snippet.html"

    party = forms.ChoiceField(choices=[])
    agent = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["party"].choices = [
            (pk, name) for pk, name in MCustomer.objects.values_list("pk", "custname")
        ]
        self.fields["agent"].choices = [
            (pk, name) for pk, name in MAgent.objects.values_list("pk", "agentname")
        ]
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
    
    size = forms.CharField(required=False, max_length=10, label="Size")
    gsm = forms.CharField(required=False, max_length=10, label="GSM")

    class Meta:
        model = TProduction
        labels = {
            "rdate": "Production Date",
            "custid": "Customer",
            "agentid": "Agent",
            "category": "Category",
            "shadecode": "Shade",
            "itemcode": "Item Code",
            "length": "Length",
            "length_unit": "Length Unit",
            "weight_unit": "Weight Unit",
            "noofbdls": "No of Bundles",
            "excise_from": "Excise From",
            "excise_to": "Excise To",
            "noofsheet": "No of Sheets",
            "noofream": "No of Reams",
            "reamwt": "Ream Weight",
            "weight": "Weight",
            "rate": "Rate",
            "locationid": "Location",
            "indentno": "Indent No",
            "lotno": "Lot No",
        }
        exclude = ("productionid", "apiflag", "fac", "stk", "approved", "entrytype", "headid","ind_weight","obflag")
        widgets = {
            "rdate": forms.DateInput(attrs={'type': 'date'}),
            "itemcode": forms.Select(attrs={
                'hx-get': reverse_lazy('invoice:TProduction_create'),
                'hx-target': '#dynform',
                'hx-trigger': 'change',
                'hx-swap': 'innerHTML',
                'hx-include': 'closest form',
            }),
            "noofbdls": forms.NumberInput(attrs={
                'hx-get': reverse_lazy('invoice:TProduction_create'),
                'hx-target': '#dynform',
                'hx-trigger': 'change',
                'hx-swap': 'innerHTML',
                'hx-include': 'closest form',
            }),
            "noofream": forms.NumberInput(attrs={
                'hx-get': reverse_lazy('invoice:TProduction_create'),
                'hx-target': '#dynform',
                'hx-trigger': 'change',
                'hx-swap': 'innerHTML',
                'hx-include': 'closest form',
            }),
            "reamwt": forms.NumberInput(attrs={
                'hx-get': reverse_lazy('invoice:TProduction_create'),
                'hx-target': '#dynform',
                'hx-trigger': 'change',
                'hx-swap': 'innerHTML',
                'hx-include': 'closest form',
            }),
            "local_or_export": forms.Select(choices=[("LOCAL", 'Local'), ("EXPORT", 'Export')]),
            "type_of_reel_sheet": forms.Select(choices=[("BUNDLE", "BUNDLE"), ("BUNDLE-LOOSE", "BUNDLE-LOOSE"), ("BULK", "BULK"), ("PALLET", "PALLET"), ("REEL", "REEL"), ("LOOSE", "LOOSE"), ("REEL-STITCHED", "REEL-STITCHED"), ("REEL-UNSTITCHED", "REEL-UNSTITCHED"), ("BUNDLE-LOOSE", "BUNDLE-LOOSE")]),
        }

class TProductionReelForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TProductionReel
        fields = "__all__"



class TStockplusminusForm(forms.ModelForm):
    """
    Form for stock plus/minus with production record chaining.
    Same fields as TProduction including excise_from and excise_to to search
    the record to update. Creates a new record with refproductionid
    instead of updating the existing one.
    """
    template_name = "form_snippet.html"

    class Meta:
        model = TProduction
        exclude = ("refproductionid", "productionid", "headid")
        widgets = {
            "rdate": forms.DateInput(attrs={'type': 'date'})
        }


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
