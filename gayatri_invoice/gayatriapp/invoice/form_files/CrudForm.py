from . import Base as bf
import json
import os
import logging
from django import forms
from ..formmod import helperFunct as hf

logger = logging.getLogger(__name__)
# TODO: have to transform this to set a form using the UI and get form.Form methods


class form_store_json:
    # INFO: creates a instance which stays till session expiry

    def __new__(self, formName, AccessRights, tables):
        logger.debug("created")
        if not hasattr(self, ".__init__"):
            self.__init__(self, formName, AccessRights, tables)

    def __init__(self, formName, AccessRights, tables):
        logger.debug("initialized")
        self.FieldDataDict = {
            "form_name": formName,
            "access_rights": AccessRights,
            "tables": tables,
            "fields": {},
        }
        self.count = 0
        self.formName = formName
        self.filename = f"form_{formName}.json"

    def addField(self, fieldtype, label, attr, var, FieldNo, child):
        logger.debug("field added")
        # check if the function is callable
        method = getattr(bf.base, fieldtype)  # method is the base.field
        incontainer = False
        # if field is a container then nest the form
        # and use a flag to get out of the nesting
        if SearchArray(fieldtype):
            incontainer = true  # flag
            if incontainer:
                pass
            else:
                if callable(method):
                    basemethod = {
                        "method": fieldtype,
                        "label": label + " " + FieldNo,
                        "attr": attr,
                        "variable": var,
                        "children": child,
                    }
                data = {FieldNo: basemethod}
                self.saveChange(data)

    def removeField(self, fieldno):
        self.FieldDataDict["fields"].pop(fieldno)
        # after poping field, update the fieldnos for every field after the poped field
        tempdatadict = self.FieldDataDict
        fieldStart = list(self.FieldDataDict["fields"].keys())[0]
        fields = len(self.FieldDataDict["fields"].keys())
        for i in range(fieldno + 1, fields + fieldStart):
            tempdatadict.update(
                str(i - 1), list(self.FieldDataDict["fields"].values())[i]
            )
        self.FieldDataDict = tempdatadict

    def edit_field(self):
        # TODO: edit the field configuration when user click on field settings
        # button get the fieldno from then set the field variables
        pass

    def SearchArray(self, field):
        # wanted to separate the container type tags for nesting
        containerlist = [
            "Container",
            "columnContainer",
            "modalContainer",
            "fieldsetContainer",
        ]
        for i in containerlist:
            if field == i:
                return 1
            else:
                return 0

    def save_to_cache(self, formdata):
        # cache has set erase time
        cachestore.set(sessionid, self.FieldDataDict)

    def save_to_file(self, formdata, filename):
        with open(filename, "w") as file:
            json.dump(formdata, file, indent=4)
        return 0

    def delete_from_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
            if os.path.exists(filename):
                return 1
        else:
            return 0

    def saveChange(self, data):
        filedata = {}
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                filedata = json.load(file)
                filedata["fields"].update(data)
                # print(filedata)
                self.saveForm(filedata)
        else:
            self.FieldDataDict["fields"].update(data)
            self.saveForm(self.FieldDataDict)

    def getFormData(self):
        with open(self.filename, "r") as file:
            filedata = json.load(file)
            return filedata


class fieldAdd(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    field_name = forms.ChoiceField(
        widget=forms.Select, choices=hf.getInputFields(formComponents), required=True
    )
    var_name = forms.CharField(required=True)
    disabled = forms.ChoiceField(widget=forms.CheckboxInput, required=True)
    table_row = forms.IntegerField(required=True)
    table_column = forms.IntegerField(required=True)


class formCreate(forms.Form):
    # Group.objects.all(), Table.objects.all()
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    form_name = forms.CharField(required=True)
    # TODO: this statement interferes with migrations
    group_names = forms.MultipleChoiceField(
        widget=forms.SelectMultiple, choices=Group.objects.values_list(), required=True
    )
    table_names = forms.MultipleChoiceField(
        widget=forms.SelectMultiple, choices=TableName.objects.all(), required=True
    )
    description = forms.CharField(required=True)


class formDelete(forms.Form):
    # search field
    template_name = "form_snippet.html"
    form_name = forms.ChoiceField(widget=forms.Select, choices="")
    group_name = forms.ChoiceField()


class formEdit(forms.Form):
    template_name = "form_snippet.html"
    form_name = forms.ChoiceField(widget=forms.Select, choices="")
    group_name = forms.ChoiceField()
    # attr=f'hx-get="/invoice/form_setup" hx-vals={jsonvalue} hx-target="none" hx-swap="none"',
    # attr='onclick=document.getElementById("modalView").style.display="none"',

