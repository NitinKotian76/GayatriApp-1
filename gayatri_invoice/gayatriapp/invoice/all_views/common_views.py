from ..formmod import CrudReport as cr
from ..formmod import CrudTable as ct
from django.shortcuts import render
from django.forms import formset_factory
import logging

logger = logging.getLogger(__name__)
# have to register the form for the formset
FORMS_MAP = {
    "reportKeyValueForm": cr.reportKeyValueForm,
    "table_metadata": ct.table_metadata,
}


def add_formset_field(request, formname: str):
    keyValueForm = FORMS_MAP.get(formname)
    keyValueFormset = formset_factory(keyValueForm, extra=0)
    if request.method == "POST" and request.POST.get("add"):
        data = request.POST.copy()
        total_forms = int(data.get("form-TOTAL_FORMS", 0))
        data["form-TOTAL_FORMS"] = str(total_forms+1)

        formset = keyValueFormset(data)
    else:
        formset = keyValueFormset()

    context = {"formset": formset, "formset_form": formname}
    return render(request, "partials/formset.html", context)
