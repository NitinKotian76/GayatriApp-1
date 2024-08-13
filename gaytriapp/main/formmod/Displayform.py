from . import BaseForm as bf
from . import CreateForm as cf
# DisplayForm returns html strings

class DisplayForm():
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
     BF.textInput("Username")+BF.password("Password")+
     BF.list("select Company:",attr='style="width:52%;"')+
     BF.button("Login",attr='id="loginbtn"')+
     BF.button("Forgot password",attr='id="forgotbtn"')
    )
  )

 def UserForm(data):
     return(
     BF.textInput("Username")+BF.password("Password")+
     BF.list("select Company:",attr='style="width:52%;"')+
     BF.button("Login",attr='id="loginbtn"')+
     BF.button("Forgot password",attr='id="forgotbtn"')
             )
 def loginSuccess():
     return(BF.modalContainer("<p>Login successful</p>"))

 def loginFail():
     return(BF.modalContainer("<p>Login failed</p>"))

 def home():
     return(BF.modalContainer('<a href="/main/login" class="w3-cell w3-button w3-blue w3-round-large">Login</a>'))

 def getBase(data):
     pass
     # match data:
     #     case clear:
     #         pass
     #     case _:
     #         print("not valid")

