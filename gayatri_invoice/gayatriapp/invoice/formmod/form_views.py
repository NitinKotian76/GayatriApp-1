from ..formmod.CrudForm import form_store_json
from ..formmod.LoadForm import Filedata

# TODO: do something about the class instance for formfield data


class form_setup:
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
