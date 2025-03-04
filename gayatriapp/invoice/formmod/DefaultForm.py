from . import BaseForm as bf
import logging

global BF, AP, inputDict, varNo
BF = bf.base
AP = bf.appControls
logger = logging.getLogger(__name__)


def addFieldshtml():
    # ui for form creation
    return BF.container(
        children='<a href="#" class="w3-btn w3-ripple w3-cell w3-blue" hx-get="/invoice/field_setup" hx-target="#modalView" hx-swap="innerHTML" onclick=document.getElementById("modalView").style.display="block">add field</a><a href="#" class="w3-btn w3-ripple w3-cell w3-blue" hx-get="/invoice/field_setup" hx-target="#modalView" hx-swap="innerHTML">add Column</a>'
    )


def loginFormhtml(company, error):
    # ui for form display
    attr1, attr2 = "", ""
    if error == 1:
        attr1 = ""
        attr2 = 'style="display:none"'

    elif error == 2:
        attr2 = ""
        attr1 = 'style="display:none"'

    else:
        attr1 = attr2 = 'style="display:none"'

    return BF.modalContainer(
        children=BF.container(
            children=BF.textInput(label="Emp Id", attr="required", valid=True)
            + BF.password(
                label="Password", attr='required class=" w3-border"', valid=False
            )
            + BF.label(label="User name or password wrong", attr=attr1)
            + BF.list(
                children=company,
                label="Select Company:",
                attr='required style="width:auto;"',
            )
            + BF.label(label="User is not from this company", attr=attr2)
            + BF.button(label="Login", attr='id="loginbtn"')
            + BF.button(label="Forgot password", attr='id="forgotbtn"')
        ),
        attr='style="display:block;"',
        cssclass="w3-display-middle w3-half",
    )


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


def formConfightml(user, table):
    # this is the config page for the fields
    # should contain the label, variable name, default value,
    logger.debug("this is entered %s %s", user, table)
    return (
        BF.textInput(label="Form Name", attr="required")
        + BF.list(label="User Name", attr="", children=user)
        + BF.fieldsetContainer(
            label="Permissions",
            children=BF.checkbox(label="Read") + BF.checkbox(label="Write"),
        )
        + BF.list(label="Tables", attr="multiple", children=table)
        + BF.textInput(label="Description", attr="")
        + BF.button(
            label="Submit",
            attr='hx-post="/invoice/form_setup" \
            hx-target="#mainform" \
            hx-swap="innerHTML" \
            onclick=document.getElementById("modalView").style.display="none"',
        )
        + BF.button(
            label="Cancel",
            attr='onclick=document.getElementById("modalView").style.display="none"',
        )
    )


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
