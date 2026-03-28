from ..models import (MAgent, MCustomer, MUnit,
                      MExportFields, MItem, MItemCategory,
                      MLocation, MPlusMinusHead, MShade)
from ..models import (TExport, TExportDetails,
                      TInvoice, TProduction, TProductionReel)
from ..models import Company
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


class CompanyForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = Company
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        htmx_attrs = {
            "hx-get": reverse_lazy('invoice:MItem_create'),
            "hx-target": '#dynform',
            "hx-trigger": 'change',
            "hx-swap": 'outerHTML',
        }
        for field in ("shadeid", "size", "gsm"):
            self.fields[field].widget.attrs.update(htmx_attrs)

    class Meta:
        model = MItem
        fields = "__all__"
        widgets = {
            "shadeid": forms.Select(),
            "size": forms.TextInput(),
            "gsm": forms.TextInput(),
        }


class MShadeForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MShade
        fields = "__all__"
        widgets = {
            "fieldgroup": forms.Select(choices=[("gsm", "GSM"), ("bdls", "BDLS"),]),

        }


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


class ProductionApprovalFilterForm(forms.Form):
    """Filter form for Production Approval: filter by rdate (reuses TProduction-style field)."""
    template_name = "form_snippet.html"
    rdate = forms.DateField(
        required=False,
        label="Production Date",
        widget=forms.DateInput(attrs={"type": "date", "id": "filter"}),
    )


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
        exclude = ("invoiceid", "apiflag", "fsc",
                   "stk", "productionid", "ind_weight")
        widgets = {
            "invoicedate": forms.DateInput(attrs={'type': 'date'}),
            "predate": forms.DateInput(attrs={'type': 'date'}),
            "remdate": forms.DateInput(attrs={'type': 'date'}),
            "lrdate": forms.DateInput(attrs={'type': 'date'}),
            "pretime": forms.TimeInput(attrs={'type': 'time'}),
            "remtime": forms.TimeInput(attrs={'type': 'time'}),
            "custid": forms.Select(attrs={
                'hx-get': reverse_lazy('invoice:TInvoice_create'),
                'hx-target': '#dynform',
                'hx-trigger': 'change',
                'hx-swap': 'innerHTML',
                'hx-include': 'closest form',
            }),
            "agentid": forms.Select(attrs={
                # 'hx-get': reverse_lazy('invoice:TInvoice_productionreel_list'),
                # 'hx-target': '#reelview',
                # 'hx-trigger': 'change delay:400ms',
                # 'hx-swap': 'innerHTML',
                # 'hx-include': 'closest form',
            }),
            "shadeid": forms.Select(attrs={
                'hx-get': reverse_lazy('invoice:TInvoice_productionreel_list'),
                'hx-target': '#reelview',
                'hx-trigger': 'change',
                'hx-swap': 'innerHTML',
                'hx-include': 'closest form',
            }),
        }


class TProductionForm(forms.ModelForm):
    template_name = "form_snippet.html"

    size = forms.CharField(required=False, max_length=10, label="Size")
    gsm = forms.CharField(required=False, max_length=10, label="GSM")

    def __init__(self, *args, htmx_get_url=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Use provided URL (update/stock+/-) or default to create; set in __init__ so update gets correct endpoint
        hx_get_url = htmx_get_url if htmx_get_url is not None else str(
            reverse_lazy("invoice:TProduction_create"))
        htmx_attrs = {
            "hx-get": hx_get_url,
            "hx-target": "#dynform",
            "hx-trigger": "change",
            "hx-swap": "outerHTML",
            "hx-include": "closest form, #formula",
        }
        for name in ("itemcode", "noofbdls", "noofsheet", "noofream", "reamwt"):
            if name in self.fields:
                self.fields[name].widget.attrs.update(htmx_attrs)

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
            "reamwt": "Stream Weight",
            "weight": "Weight",
            "rate": "Rate",
            "locationid": "Location",
            "indentno": "Indent No",
            "lotno": "Lot No",
        }
        exclude = ("productionid", "apiflag", "fsc", "stk",
                   "approved", "entrytype", "headid", "ind_weight", "obflag")
        # HTMX attrs for itemcode/noofbdls/noofsheet/noofream/reamwt are set in __init__ (create vs update URL)
        widgets = {
            "custid": forms.Select(attrs={
                'hx-get': reverse_lazy('invoice:TProduction_create'),
                'hx-target': '#dynform',
                'hx-trigger': 'change',
                'hx-swap': 'innerHTML',
                'hx-include': 'closest form',
            }),
            "rdate": forms.DateInput(attrs={'type': 'date'}),
            "itemcode": forms.Select(),
            "noofbdls": forms.NumberInput(),
            "noofsheet": forms.NumberInput(),
            "noofream": forms.NumberInput(),
            "reamwt": forms.NumberInput(),
            "local_or_export": forms.Select(choices=[("LOCAL", 'Local'), ("EXPORT", 'Export')]),
            "type_of_reel_sheet": forms.Select(choices=[("BUNDLE", "BUNDLE"), ("BUNDLE-LOOSE", "BUNDLE-LOOSE"), ("BULK", "BULK"), ("PALLET", "PALLET"), ("REEL", "REEL"), ("LOOSE", "LOOSE"), ("REEL-STITCHED", "REEL-STITCHED"), ("REEL-UNSTITCHED", "REEL-UNSTITCHED"), ("BUNDLE-LOOSE", "BUNDLE-LOOSE")]),
        }


class TProductionReelForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TProductionReel
        fields = "__all__"


class RStockForm(forms.Form):

    template_name = "form_snippet.html"
    choices = [(1, "all"), (2, "group by category")]
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    type_of_report = forms.ChoiceField(choices=choices)


class RDispatchForm(forms.Form):

    template_name = "form_snippet.html"
    choices = [(1, "all"), (2, "party wise")]
    from_date = forms.DateField()
    to_date = forms.DateField()
    party = forms.ChoiceField(choices=[])
    type_of_report = forms.ChoiceField(choices=[])

    def __init__(self):
        self.fields["party"].choices = MCustomer.objects.all()

    class Meta:
        widgets = {
            "date": forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            )
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
