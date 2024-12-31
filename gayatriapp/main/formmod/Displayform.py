from . import DefaultForm as df
from . import CrudForm as cf
# DisplayForm returns html strings

class DisplayForm():
    def LoadForms(self): 
       return cf.formFieldData().getFormData()

    def loadDraftForms(self):
        pass

