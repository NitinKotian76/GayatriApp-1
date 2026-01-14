from ..models import (MAgent, MCategory, MCompany, MCustomer, MEmployee,
                      MExportFields, MItem, MItemCategory, MItemRate,
                      MLocation, MPlusMinusHead, MShade, MSupplier)
from ..models import (TempDP, TempWeightSlip, TExport, TExportDetails, TIndent,
                      TInvoice, TJumboRollWiseQC, TLOTNoWiseQc, TProduction,
                      TProduction_bck, TProductionReel, TWB)
from django import forms


class MAgentForm(forms.ModelForm):
    class Meta:
        model = MAgent
        fields = "__all__"

    template_name = "form_snippet.html"
