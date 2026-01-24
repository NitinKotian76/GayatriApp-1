from ..models import (MAgent, MCategory, MCustomer, MEmployee,
                      MExportFields, MItem, MItemCategory, MItemRate,
                      MLocation, MPlusMinusHead, MShade, MSupplier)
from ..models import (TExport, TExportDetails, TIndent,
                      TInvoice, TJumboRollWiseQC, TLOTNoWiseQc, TProduction,
                      TProduction_bck, TProductionReel)
from ..models import RChallan
from django import forms


class MAgentForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MAgent
        fields = "__all__"


class MCategoryForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MCategory
        fields = "__all__"


class MCustomerForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MCustomer
        fields = "__all__"


class MEmployeeForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MEmployee
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


class MItemRateForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = MItemRate
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


class TIndentForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TIndent
        fields = "__all__"


class TInvoiceForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TInvoice
        fields = "__all__"


class TJumboRollWiseQCForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TJumboRollWiseQC
        fields = "__all__"


class TLOTNoWiseQcForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TLOTNoWiseQc
        fields = "__all__"


class TProductionForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = TProduction
        fields = "__all__"


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


class RChallanForm(forms.ModelForm):
    template_name = "form_snippet.html"

    class Meta:
        model = RChallan
        fields = "__all__"
