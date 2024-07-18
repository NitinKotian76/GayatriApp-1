from . import BaseForm as bf
from django.template.loader import render_to_string 
from django.utils.html import format_html
from .. import views 
# DisplayForm returns html strings

class DisplayForm():
 global BF, AP, inputDict, varNo
 BF = bf.base
 AP = bf.appControls
 
 def show(data):
  inputs =  BF.checkbox(data)
  return BF.form(inputs+AP.add())

 def loginForm(*args, **kwargs):
  csrf = kwargs.get('csrf', None)
  return (
   BF.modalContainer(BF.form(
     BF.textInput("User Name")+BF.password("Password")+
     BF.list("select Company:",attr='style="width:50%;"')+
     BF.button("Login",attr='id="loginbtn"')+
     BF.button("Forgot password",attr='id="forgotbtn"')
    ),
     attr='id="login" action="/main"',
     csrf=csrf,
   )
  )

