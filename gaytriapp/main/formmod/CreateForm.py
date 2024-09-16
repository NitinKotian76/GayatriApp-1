"""
when clicked the method should already have a draft file saved in the path
the click should only trigger an append function and the draft form should be saved
the next click should do the same 
"""

from . import BaseForm as bf
from main import models 
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

    def addField(self,field,args,var,FieldNo):
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
        method = getattr(bf.base,field)
        if callable(method):
            basemethod = {
                    "method":field,
                    "arguments":args,
                    "variable":var,
            }
            # fieldname ="field"+FieldNo
            data={FieldNo: basemethod}
            self.AddDatatoDraft(data)

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
        with open(self.draftfilename,'r') as file:
            filedata=json.load(file)
            return filedata
