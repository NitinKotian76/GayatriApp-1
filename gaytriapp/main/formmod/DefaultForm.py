from . import BaseForm as bf
 
global BF, AP, inputDict, varNo
BF = bf.base
AP = bf.appControls

def AddFields():
 # ui for form creation
 return (AP.getInputFields())

def loginForm():
# ui for form display
 return (
  BF.modalContainer(
    BF.textInput(label="Username")+BF.password(label="Password")+
    BF.list(label="select Company:",attr='style="width:52%;"')+
    BF.button(label="Login",attr='id="loginbtn"')+
    BF.button(label="Forgot password",attr='id="forgotbtn"')
   )
 )
def loginSuccess():
    return(BF.modalContainer("<p>Login successful</p>"))

def loginFail():
    return(BF.modalContainer("<p>Login failed</p>"))

def home():
    return(BF.modalContainer('<a href="/main/login" class="w3-cell w3-button w3-blue w3-round-large">Login</a>'))
