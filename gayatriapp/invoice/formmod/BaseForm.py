from django.utils.html import format_html
from django.template import Template
from django.http import JsonResponse
from django import forms


def getInputFields():
    methods_list = [
        method
        for method in dir(forms)
        if callable(getattr(forms, method)) and not method.startswith("__")
    ]
    return methods_list


# class base:
#     global ButtonStyle, InputStyle, RowCellStyle, RowStyle, leftSpace, globalSpacing, TextAlignCenter, cellSpacing
#     ButtonStyle = " w3-cell w3-button w3-blue w3-round-large w3-ripple"
#     globalSpacing = " w3-margin"
#     cellSpacing = " w3-padding"
#     leftSpace = " w3-margin-left"
#     TextAlignCenter = " w3-center"
#     InputStyle = " w3-card"


class open_bal_prod(forms.Form):
    template_name = "form_snippet.html"
    date = forms.DateField()
    plus_minus_head = forms.ChoiceField(choices=("plus", "minus"))
    local_or_export = forms.ChoiceField(choices=("local", "export"))
    variety = forms.ChoiceField()
    type = forms.ChoiceField()
    item_code = forms.ChoiceField()
    size = forms.DecimalField()
    length = forms.DecimalField()
    gsm = forms.IntegerField()
    unit = forms.ChoiceField()
    no_of_bdls = forms.ChoiceField()  # no of bundles
    excise_no_from = forms.IntegerField()
    excise_no_to = forms.IntegerField()
    no_of_sheets = forms.IntegerField()
    ream_weight = forms.DecimalField()
    no_of_ream = forms.IntegerField()
    weight = forms.DecimalField()
    rate = forms.DecimalField()
    location = forms.ChoiceField()
    indent_no = forms.IntegerField()
    party = forms.ChoiceField()
    agent = forms.ChoiceField()
    fsc = forms.ChoiceField(choices=("yes", "no"))
    lot_no = forms.IntegerField()
    # tableview()
