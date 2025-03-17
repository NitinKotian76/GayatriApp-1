from . import BaseForm as bf
from django import forms
import logging
from ..models import *

global BF, AP, inputDict, varNo
BF = bf.base
AP = bf.appControls
logger = logging.getLogger(__name__)


class loginForm(forms.Form):
    template_name = "form_snippet.html"
    empid = forms.IntegerField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    cmpname = forms.ChoiceField(
        widget=forms.Select, choices=Company.objects.values_list(), required=True
    )
    # attr='style="display:block;"',
    # cssclass="w3-display-middle w3-half",


def logouthtml():
    return BF.modalContainer(
        children="<p>Logout successful</p>",
        attr='style="display:block;"',
        cssclass="w3-center w3-padding w3-margin",
    )


def profilehtml(user):
    return BF.modalContainer(
        attr='style="display:block;"',
        children=BF.button(
            label="x",
            attr='onclick=this.style.display="none"',
            cssclass="w3-display-topright",
        )
        + BF.label(label="Name")
        + BF.label(label="groups"),
    )


# edit the fields


class formConfig(forms.Form):
    # Group.objects.all(), Table.objects.all()
    template_name = "form_snippet.html"
    form_name = forms.CharField()
    group_name = forms.MultipleChoiceField(
        widget=forms.SelectMultiple, choices=Group.objects.values_list()
    )
    table_names = forms.MultipleChoiceField(
        widget=forms.SelectMultiple, choices=Table.objects.values_list()
    )
    description = forms.CharField()


def fieldConfightml():
    itemlist = AP.getInputFields()
    return (
        BF.modalContainer(
            children=BF.list(children=itemlist, label="Field Name")
            + BF.textInput(label="Variable Name")
            + BF.checkbox(label="Disabled")
            + BF.list(label="Table Row")
            + BF.list(label="Table Column")
            + BF.button(
                label="Submit",
                attr='hx-post="/invoice/field_setup" hx-target="#mainform" hx-swap="none"',
            )
            + BF.button(
                label="Cancel",
                attr='onclick=document.getElementById("modalView").style.display="none"',
            )
        ),
    )


def formDeletehtml():
    # forms  = getForms.formname()
    # groups = getForms.formgroups()
    # descs   = getForms.formdesc()
    # for form in forms:
    #     formlist = f'<td>group<td>'
    # for group in groups:
    #     grouplist = f'<td>group</td>'
    # for desc in descs:
    #     desclist = f'<td>desc</td>'
    formlistview = f'<div class="w3-table"><tr><th>Form Name</th><th>Groups</th><th>Description</th></tr><tr>formlist</tr><tr>grouplist</tr><tr>desclist</tr></div>'
    jsonvalue = "{'view': 'formdelete'}"
    return (
        BF.modalContainer(
            children=formlistview
            + BF.button(
                label="Delete",
                attr=f'hx-get="/invoice/form_setup" hx-vals={jsonvalue} hx-target="none" hx-swap="none"',
            )
            + BF.button(
                label="Cancel",
                attr='onclick=document.getElementById("modalView").style.display="none"',
            )
        ),
    )


def formEdithtml():
    # forms  = getForms.formname()
    # groups = getForms.formgroups()
    # descs   = getForms.formdesc()
    # for form in forms:
    #     formlist = f'<td>group<td>'
    # for group in groups:
    #     grouplist = f'<td>group</td>'
    # for desc in descs:
    #     desclist = f'<td>desc</td>'
    formlistview = f'<div class="w3-table"><tr><th>Form Name</th><th>Groups</th><th>Description</th></tr><tr>formlist</tr><tr>grouplist</tr><tr>desclist</tr></div>'
    jsonvalue = "{'view': 'formedit'}"
    return (
        BF.modalContainer(
            children=formlistview
            + BF.button(
                label="Edit",
                attr=f'hx-get="/invoice/form_setup" hx-vals={jsonvalue} hx-target="none" hx-swap="none"',
            )
            + BF.button(
                label="Cancel",
                attr='onclick=document.getElementById("modalView").style.display="none"',
            )
        ),
    )
