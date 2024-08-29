from . import DefaultForm as df
from . import CreateForm as cf
# DisplayForm returns html strings

class DisplayForm():
    def LoadForms(self): 
       return cf.formFieldData().getFormData()

    def loadDraftForms(self):
        pass

class displayDefaultForms():

    def addFields(self):
        return df.AddFields()
    def loginForm(self):
        return df.loginForm()
    def loginSuccess(self):
        return df.loginSuccess()
    def loginFail(self):
        return df.loginFail()
    def home(self):
        return df.home()
