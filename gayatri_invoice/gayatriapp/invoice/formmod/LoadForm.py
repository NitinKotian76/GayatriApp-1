import logging
from ..models import TableData


# NOTE: can use type to create forms dynamically
# dyn_form = type(form_name,(forms.Form,),{baseFields:fields})
#

def Filedata(filename):
    """
    the purpose of this function should be to get the json data form file and
    create a list of input fields with htmx attributes
    """

    logger = logging.getLogger(__name__)
    with open(filename, "r") as file:
        data = json.load(file)
        logger.debug(data)
        htmllist = []
        html = ""
        for i in range(len(data["fields"].keys())):
            fields = list(data["fields"].keys())
            method = getattr(base, data["fields"][fields[i]]["method"])
            # print(data["fields"][fields[i]]["attr"])
            # print(data["fields"][fields[i]]["label"])
            label = data["fields"][fields[i]]["label"]
            attr = data["fields"][fields[i]]["attr"]
            child = data["fields"][fields[i]]["children"]
            field = method(children=child, label=label, attr=attr)
            htmllist.append(field)
        # print(htmllist)
        for i in range(len(htmllist)):
            # print(htmllist[i])
            html += htmllist[i]
        print(type(html))
        return html
