from . import DefaultForm as df
# DisplayForm returns html strings

class DisplayForm():
    def displayLoadedForms():
        pass
    def displayDraftForms():
        pass

class displayDefaultForms():

    def addFields():
        return df.AddFields()
    def loginForm():
        return df.loginForm()
    def userForm():
        return df.UserForm()
    def loginSuccess():
        return df.loginSuccess()
    def loginFail():
        return df.loginFail()
    def home():
        return df.home()
