"""
when clicked the method should already have a draft file saved in the path
the click should only trigger an append function and the draft form should be saved
the next click should do the same 
"""

from . import BaseForm as bf
import tempfile
import json
import os
# crud

class formFieldData:
    """ 
    processes the field selections from user input

    Attributes
    ----------
    FieldDataDict : default form constants and variable
    count : no of fields
    filename : filename
    draftfilename : draft file name 
    """
    def __init__(self,formName,AccessRights,tables):
        self.FieldDataDict = {
                "form_name": formName,
                "access_rights" : AccessRights,
                "tables" : tables,
                "fields" : {} 
        }
        self.count = 0
        self.filename= f"form_{formName}.json"
        # self.draftfilename = f"draftForm_{formName}.json"

    def removeField(self,fieldno):
        self.FieldDataDict["fields"].pop(fieldno)
        # after poping field update the fieldnos for every field after the poped field
        tempdatadict = self.FieldDataDict
        fieldStart = list(self.FieldDataDict["fields"].keys())[0]
        fields = len(self.FieldDataDict["fields"].keys())
        for  i in range(fieldno+1,fields+fieldStart):
            tempdatadict.update(str(i-1),list(self.FieldDataDict["fields"].values())[i])
        self.FieldDataDict = tempdatadict


    def addField(self,field,label,attr,var,FieldNo,child):
        """
        addfield to a dictionary and save the file using json

        Parameters
        ----------
        field : field name
            
        args : any arguments passed to the field 
            
        var : any variables assigned to the field            

        FieldNo : fieldno/ id

        """
        # check if the function is callable
        method = getattr(bf.base,field) # method is the base.field
        incontainer = False
        # if field is a container then nest the form 
        # and use a flag to get out of the nesting 
        if(SearchArray(field)):
            incontainer = true # flag
            if incontainer :
                pass
            else :
                if callable(method):
                    basemethod = {
                            "method":field,
                            "label":label,
                            "attr":attr,
                            "variable":var,
                            "children":child
                    }
                data={FieldNo: basemethod}
                self.AddDatatoDraft(data)

    def SearchArray(self,field):
        containerlist = ['Container','columnContainer','modalContainer','fieldsetContainer']
        for i in containerlist:
            if field == i:
                return 1
            else:
                return 0

    def saveForm(self,formdata):
        with open(self.filename,'w') as file:
            json.dump(formdata,file,indent=4)

    def deleteForm(self,filename):
        if os.path.exists(filename):
            os.remove(filename)


    def AddDatatoDraft(self,data):
        """
        this function will add to the dictionary in the json file

        Returns
        -------
        none
        """
        filedata = {}
        if os.path.exists(self.filename):
            with open(self.filename,'r') as file:
                filedata=json.load(file)
                filedata["fields"].update(data)
                # print(filedata)
                self.saveForm(filedata)
        else:
            self.FieldDataDict["fields"].update(data)
            self.saveForm(self.FieldDataDict)

    def getFormData(self):  
        """
        Returns
        -------
        the field dictionary
            
        """
        with open(self.filename,'r') as file:
            filedata=json.load(file)
            return filedata
