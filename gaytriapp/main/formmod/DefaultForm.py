from . import BaseForm as bf
 
global BF, AP, inputDict, varNo
BF = bf.base
AP = bf.appControls

def AddFields():
 # ui for form creation
 return (AP.getInputFields())

def loginForm():
# ui for form display
 company = ['company1','company2','company3']
 return (
  BF.modalContainer(children=BF.textInput(label="Username")+BF.password(label="Password")+
    BF.list(company,label="select Company:",attr='style="width:52%;"')+
    BF.button(label="Login",attr='id="loginbtn"')+
    BF.button(label="Forgot password"),
    attr='id="forgotbtn" style="display:block;"'
   )
 )
def loginSuccess():
    return(BF.modalContainer(children="<p>Login successful</p>",attr='style="display:block;"'))

def loginFail():
    return(BF.modalContainer(children="<p>Login failed</p>",attr='style="display:block;"'))

def home():
    return(BF.modalContainer(children='<a href="/main/login" class="w3-cell w3-button w3-blue w3-round-large">Login</a>', attr='style="display:block;"'))
# edit the field
def formSetup():
    # this is the config page for the fields 
    # should contain the label, variable name, default value, 
    childlist = ['user1','user2','user3']
    return(BF.modalContainer(children=BF.fieldsetContainer(children=BF.textInput(label="Form Name")+
                                BF.list(label="user name",children=childlist)+
                                BF.checkbox(label="read")+BF.checkbox(label="write")+
                                BF.textInput(label="Form Name"),
                                label="Form Setup")
           ))
