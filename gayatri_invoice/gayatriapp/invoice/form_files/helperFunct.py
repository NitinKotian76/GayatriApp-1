from .LoadFunct import Filedata
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..models import *
import json
import logging
logger = logging.getLogger(__name__)


# helper functions

def getInputFields(object):
    methods_list = [
        method
        for method in dir(object)
        if callable(getattr(object, method)) and not method.startswith("__")
    ]
    return methods_list


def button(**kwargs):
    """ 
    this function specificaly uses buttons  so the attr are only which are needed
    """

    hx_req_type = kwargs.get("hx_req_type", "hx-post")
    hx_req = kwargs.get("hx_req", "")
    hx_vals = kwargs.get("hx_vals", "")
    hx_target = kwargs.get("hx_target", "")
    hx_swap = kwargs.get("hx_swap", "")
    attrs = kwargs.get("attrs", {})
    type = kwargs.get("type", "button")
    value = kwargs.get("value", "")

    attrs_html = format_html_join(" ", '{}="{}"', attrs.items())

    if hx_req == "" and hx_vals == "" and hx_target == "" and hx_swap == "": # no htmx attributes
        html = format_html("<input class='w3-button w3-ripple w3-green w3-padding w3-margin'"
                       "type='{}' value='{}' "
                       "{}/>",type, value, attrs_html)
    elif hx_vals != "": # hx-vals attribute is present
        html = format_html("<input class='w3-button w3-ripple w3-green w3-padding w3-margin'"
                           "type='{}' value='{}' "
                           "{}='{}'"
                           "hx-vals='{}'"
                           "hx-target='{}'"
                           "hx-swap='{}'"
                           "{}/>",type, value, hx_req_type, hx_req,
                           json.dumps(hx_vals),
                           hx_target, hx_swap, attrs_html)
    else: #with htmx attributes
        html = format_html("<input class='w3-button w3-ripple w3-green w3-padding w3-margin'"
                           "type='{}' value='{}' "
                           "{}='{}'"
                           "hx-target='{}'"
                           "hx-swap='{}'"
                           "{}/>",type, value, hx_req_type, hx_req,
                           hx_target, hx_swap, attrs_html)

    return html


def btn_append(handler: dict, item: str) -> str:
    """
    append the list of buttons
        Args:
        handler = dict of objects
        item = the name of the dict of items

        returns:
        buttons = appended list of button html fragments

    """
    buttons = []
    for key in handler[item]:
        call_args = {}
        if handler[item][key].get("type"):
            call_args["type"] = handler[item][key].get("type")

        if handler[item][key].get("value"):
            call_args["value"] = handler[item][key].get("value")

        if handler[item][key].get("hx_req_type"):
            call_args["hx_req_type"] = handler[item][key].get("hx_req_type")

        if handler[item][key].get("hx_vals"):
            call_args["hx_vals"] = handler[item][key].get("hx_vals")

        if handler[item][key].get("hx_req"):
            call_args["hx_req"] = handler[item][key].get("hx_req")

        if handler[item][key].get("hx_swap"):
            call_args["hx_swap"] = handler[item][key].get("hx_swap")

        if handler[item][key].get("hx_target"):
            call_args["hx_target"] = handler[item][key].get("hx_target")

        if handler[item][key].get("attrs"):
            call_args["attrs"] = handler[item][key].get("attrs")

        # adds all the args for the current item
        btn = button(**call_args)
        buttons.append(btn)
    return buttons


def file_handler(name, file):
    # TODO: properly handle Files

    path = default_storage.save(f"ReportTemplates/{name}", file)
    logger.debug(default_storage.size(path))


class form_setup:
    # TODO: do something about the class instance for formfield data
    def __init__(self):
        self.ff = None

    def create_form(self, *args, **kwargs):
        tables = {"tables": TableNames}
        ff = form_store_json(formName, Access_rights, tables)

    def save_to_db(self, *args, **kwargs):
        ff.saveForm(ff.FieldDataDict)
        logger.debug("form saved")
        return JsonResponse({"success": True, "message": "form saved successfully"})

    def delete_form_db(self, *args, **kwargs):
        pass

    def edit_form(self, *args, **kwargs):
        logger.debug(df.addFields())
        return HttpResponse(df.addFields())

    def add_field(self, *args, **kwargs):
        fieldtype = kwargs.get("fieldtype", "")
        label = kwargs.get("label", "")
        attr = kwargs.get("attr", "")
        form = kwargs.get("form", "")
        fieldno = kwargs.get("fieldno", "")
        # TODO:have to figure out a way to add list data from selected table
        child = kwargs.get("data", "")
        ff.addField(fieldtype, label, attr, form, fieldno, child)
        return HttpResponse(Filedata(ff.filename))

    def save_field_config(self, *args, **kwargs):
        if request.method == "POST":
            ff = formFieldData(formname, permissions, tables)

    def rm_field(self, *args, **kwargs):
        fieldno = request.POST.get("rm_field")
        ff.removeField(fieldno)
        request.session["count"] = request.session.get("count", 0) - 1
        print(request.session.get("count", 0))
        return HttpResponse(Filedata(ff.filename))

    def calculatevalue(self, *args, **kwargs):
        # called on a result field
        # this would sipmlify the calculation part
        # and when save is clicked the value will be saved
        pass

    def link_data_field(self, *args, **kwargs):
        # the field is linked via varname which is stored in a vartable which is searched for the value and
        # is poulated to the link destination can be asked by a report or a form
        # this poses another problem if the link source name is changed the link dest will be floating
        # this should be resolved by throwing error to the user and showing which forms link source is
        # responsible for the error which  means the vartable has to store the varname and the formname of the varname.
        pass

    def cancel(self):
        return HttpResponse("")
