from . import BaseForm as bf
import json
import os
import logging

# crud
logger = logging.getLogger(__name__)
class formFieldData():
    def __new__(self,formName,AccessRights,tables):
        logger.debug("created")
        if not hasattr(self,'.__init__'):
            self.__init__(self,formName,AccessRights,tables)
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
        logger.debug("initialized")
        self.FieldDataDict = {
                "form_name": formName,
                "access_rights" : AccessRights,
                "tables" : tables,
                "fields" : {} 
        }
        self.count = 0
        self.formName= formName
        self.filename= f"form_{formName}.json"

    # crud for form fields #
    #______________________#
    def addField(self,fieldtype,label,attr,var,FieldNo,child):
        """
        addfield to a dictionary and save the file using json
        the function is called every time user click on add button 
   
        Parameters
        ----------
        field : field name
            
        args : any arguments passed to the field 
            
        var : any variables assigned to the field            

        FieldNo : fieldno/ id

        """
        logger.debug("field added")
        # check if the function is callable
        method = getattr(bf.base,fieldtype) # method is the base.field
        incontainer = False
        # if field is a container then nest the form 
        # and use a flag to get out of the nesting 
        if(SearchArray(fieldtype)):
            incontainer = true # flag
            if incontainer :
                pass
            else :
                if callable(method):
                    basemethod = {
                            "method":fieldtype,
                            "label":label+" "+FieldNo,
                            "attr":attr,
                            "variable":var,
                            "children":child
                    }
                data={FieldNo: basemethod}
                self.saveChange(data)

    def removeField(self,fieldno):
        self.FieldDataDict["fields"].pop(fieldno)
        # after poping field update the fieldnos for every field after the poped field
        tempdatadict = self.FieldDataDict
        fieldStart = list(self.FieldDataDict["fields"].keys())[0]
        fields = len(self.FieldDataDict["fields"].keys())
        for  i in range(fieldno+1,fields+fieldStart):
            tempdatadict.update(str(i-1),list(self.FieldDataDict["fields"].values())[i])
        self.FieldDataDict = tempdatadict

    def edit_field(self):
        #TODO: edit the field configuration when user click on field settings button get the fieldno from then set the field variables
        pass

    def SearchArray(self,field): ## wanted to seperate the container type tags for nesting
        containerlist = ['Container','columnContainer','modalContainer','fieldsetContainer']
        for i in containerlist:
            if field == i:
                return 1
            else:
                return 0

    def save_to_cache(self,formdata):
        ''' cache has set erase time '''
        cachestore.set(sessionid,self.FieldDataDict)

    def save_to_file(self,formdata,filename):
        with open(filename,'w') as file:
            json.dump(formdata,file,indent=4)
        return 0

    def delete_from_file(self,filename):
        if os.path.exists(filename):
            os.remove(filename)
            if os.path.exists(filename):
                return 1
        else:
            return 0

    def saveChange(self,data):
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
