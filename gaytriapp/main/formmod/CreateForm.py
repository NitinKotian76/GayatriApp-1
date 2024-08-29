from . import BaseForm as bf
import tempfile
import json
import os
# crud

class formFieldData:

    def setField(self,formName,AccessRights,tables):
        self.FieldDataDict = {
                "form_name": formName,
                "access_rights" : AccessRights,
                "tables" : tables,
                "fields" :{} 
                }
        self.count = 0

    def removeField(self):
        pass

    def addField(self,field,args,var):
        method = getattr(bf.base,field)
        if callable(method):
            basemethod = {
                    "method":field,
                    "arguments":args,
                    "variable":var,
            }
            fieldnum = "field %s" % self.count
            self.FieldDataDict['fields'][fieldnum] = basemethod 
            print(self.count ,self.FieldDataDict)



    def saveForm(self,formdata,formname="data.json"):
        with open(formname,'w') as file:
            file.write(json.dumps(formdata,indent=4))

    def deleteForm(self,formname="data.json"):
        if os.path.exists(formname):
            os.remove(formname)

    def saveDraft(self,formdata,formname="data.json.draft"):
        with open(formname,'w') as file:
            file.write(json.dumps(formdata,indent=4))
    
    def saveTempData(self,formdata,formname= "temp"):
        with tempfile.TemporaryFile() as tfile:
            tfile.write(bytes(json.dumps(formdata),encoding='utf8'))
            # tfile.seek(0)
            # print(tfile.read())
        #dictionary data for the draft

    def deleteDraft(self):
        pass


    def getFormData(self):  
        return self.FieldDataDict
