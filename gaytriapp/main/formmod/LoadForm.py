import os 
import json 
from .BaseForm import base


def Filedata(filename):
    """the purpose of this function should be to get the json data form file and 
    create a list of input fields with htmx attributes 
    """
    with open(filename,"r") as file:
        data = json.load(file)
        print(data)
        htmllist = []
        html = ""
        for i in range(len(data["fields"].keys())):
            fields = list(data["fields"].keys())
            method = getattr(base,data["fields"][fields[i]]["method"])
            htmllist.append(method(data["fields"][fields[i]]["arguments"]))
        print(htmllist)
        for i in range(len(htmllist)):
            print(htmllist[i])
            html += htmllist[i]
        print(type(html))
        return html

