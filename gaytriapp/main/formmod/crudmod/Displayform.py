from . import BaseForm as bf
from django.template.loader import render_to_string


class DisplayForm():
    global BF, AP, inputDict, varNo
    BF = bf.base
    AP = bf.appControls
    inputDict = { }
    varNo = 0

    def show():
        return BF.form(AP.add())

    def htmlForm(data):
        result= ""
        
        if data['type'] == "input":
            if data['input_type']== "textinput":
                inputDict[f"input{varNo}"] = BF.text_input()
                for x in inputDict.values():
                    result += "\n" + x
                varNo += 1
                result += AP.add()
                print(result)
        return BF.form(result)
