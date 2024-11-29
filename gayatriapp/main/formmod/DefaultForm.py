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
     return (BF.modalContainer(children=BF.textInput(label="Username")+BF.password(label="Password")+
                               BF.list(company,label="select Company:",attr='style="width:52%;"')+
                               BF.button(label="Login",attr='id="loginbtn"')+
                               BF.button(label="Forgot password"),
                               attr='id="forgotbtn" style="display:block;"')
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
def formSetup():
    # this is the config page for the fields 
    # should contain the label, variable name, default value, 
    childlist = ['user1','user2','user3']
    return(
            BF.modalContainer(
                children=BF.container(
                    children=BF.form(
                        children=
                        BF.textInput(label="Form Name")+
                        BF.list(label="User Name",children=childlist)+
                        BF.container(
                            children=
                            BF.checkbox(label="Read",attr='value="1"')+
                            BF.checkbox(label="Write",attr='value="1"'))+
                        BF.textInput(label="Description",attr="")+
                        BF.button(
                            label="Submit",
                            attr='hx-post="/main/form_setup" hx-target="this" hx-swap="none"')+
                        BF.button(
                            label="Cancel",
                            attr='onclick=document.getElementById("modalView").style.display="none"')
                        ),
                    label="Form Setup",attr=''),
                attr='style="display:block"')
            )

def fieldSetup():
    return(BF.modalContainer(children=BF.container(
            children=BF.textInput(label="Field Name")+
                BF.textInput(label="Variable Name")+
                BF.checkbox(label="Disabled")+
                BF.list(label="Table Row")+
                BF.list(label="Table Column")+
                BF.button(label="Submit",attr='hx-post="/main/edit_field" ')+
                BF.button(label="Cancel",attr='onclick=document.getElementById("modalView").style.display="none"')),
                label="Field Config",attr='style="display:block"')
    )
