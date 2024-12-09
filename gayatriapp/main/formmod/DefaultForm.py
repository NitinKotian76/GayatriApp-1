from . import BaseForm as bf
 
global BF, AP, inputDict, varNo
BF = bf.base
AP = bf.appControls

def addFields():
     # ui for form creation
     return(AP.getInputFields())

def loginForm():
     # ui for form display
     company = ['company1','company2','company3']
     return (BF.modalContainer(children=BF.textInput(label="Username",attr='required')+BF.password(label="Password",attr='required')+
                               BF.list(children=company,label="select Company:",attr='required style="width:52%;"')+
                               BF.button(label="Login",attr='id="loginbtn"')+
                               BF.button(label="Forgot password",attr='id="forgotbtn"'),
                               attr='style="display:block;"')
             )
def loginSuccess():
    return(BF.modalContainer(children="<p>Login successful</p>",attr='style="display:block;"'))

def loginFail():
    return(BF.modalContainer(children="<p>Login failed</p>",attr='style="display:block;"'))

def home():
    return(BF.modalContainer(children='<a href="/main/login" class="w3-cell w3-button w3-blue w3-round-large">Login</a>',
                             attr='style="display:block;"')
           )

# edit the fieldn
def formConfig():
    # this is the config page for the fields 
    # should contain the label, variable name, default value, 
    childlist = ['user1','user2','user3']
    tablelist = ['user1','user2','user3']
    return(
            BF.container(
                    children=BF.form(
                        children=
                        BF.textInput(label="Form Name",attr='required')+
                        BF.list(label="User Name",attr='required',children=childlist)+
                        BF.fieldsetContainer(children=BF.checkbox(label="Read")+BF.checkbox(label="Write"))+
                        BF.list(label="Tables",attr='multiple',children=tablelist)+
                        BF.textInput(label="Description",attr='')+
                        BF.button(label="Submit",attr='hx-post="/main/form_setup" hx-target="#formConfig" hx-swap="outerHTML"')+
                        BF.button(label="Cancel",attr='hx-post="/main/cancel" hx-target="#formConfig" hx-swap="outerHTML"')
                        ),
                    label="Form Setup", attr='id="formConfig"')
            )

def fieldConfig():
    return(BF.container(children=BF.container(
            children=BF.textInput(label="Field Name",attr='required')+
                BF.textInput(label="Variable Name")+
                BF.checkbox(label="Disabled")+
                BF.list(label="Table Row")+
                BF.list(label="Table Column")+
                BF.button(label="Submit",attr='hx-post="/main/edit_field"')+
                BF.button(label="Cancel",attr='onclick=document.getElementById("modalView").style.display="none"')),
                label="Field Config",attr='style="display:block"')
    )

