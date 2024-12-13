from . import BaseForm as bf
 
global BF, AP, inputDict, varNo
BF = bf.base
AP = bf.appControls

def addFields():
# ui for form creation
    # itemlist = AP.getInputFields()
    # FieldList = ""
    # for item in itemlist:
    #     Field = f'<a hx-post="/main/edit_field" \
    #                  hx-target="#mainform" \
    #                  hx-swap="innerhtml" \
    #                  class="w3-bar-item w3-button fieldlist" \
    #                  id="{item}"> \
    #                  {item} \
    #                </a>'
    # <div class="w3-dropdown-content w3-bar-block w3-border">{FieldList}</div>
    #     FieldList += Field
                            
    children = f'<section><div class="w3-cell-row w3-margin-top"><div class="w3-dropdown-hover w3-cell" style="width:80%"><button type="button" class="addrow w3-cell-row w3-button w3-blue" hx-post="/main/edit_field" hx-target="#modalView" hx-swap="innerHTML">+</button></div><div class="w3-cell" style="width:20%"><button class="addcolumn w3-cell-row w3-button w3-blue" hx-post="" hx-target="" hx-swap="" >+</button></div></div></section>'

    return(BF.container(children=children))


def loginForm():
     # ui for form display
     company = ['company1','company2','company3']

     return (BF.modalContainer(children=BF.container(children=BF.textInput(label="Username",attr='required',valid=True)+
                               BF.password(label="Password",attr='required class=" w3-border"',valid=False)+
                               BF.list(children=company,label="select Company:",attr='required style="width:auto;"')+
                               BF.button(label="Login",attr='id="loginbtn"')+
                               BF.button(label="Forgot password",attr='id="forgotbtn"')),
                               attr='style="display:block;"',cssclass="w3-display-middle w3-half")
             )

def loginSuccess():
    return(BF.modalContainer(children="<p>Login successful</p>",attr='style="display:block;"'))

def loginFail():
    return(BF.modalContainer(children="<p>Login failed</p>",attr='style="display:block;"'))

def logedout():
    return(BF.modalContainer(children="<p>Logout successful</p>",attr='style="display:block;"'))

def home():
    return(BF.modalContainer(children='<a href="/main/login" class="w3-cell w3-button w3-blue w3-round-large w3-display-middle">Login</a>',
                             attr='style="display:block;"',cssclass="w3-display-middle")
           )

# edit the fieldn
def formConfig():
    # this is the config page for the fields 
    # should contain the label, variable name, default value, 
    childlist = ['user1','user2','user3']
    tablelist = ['user1','user2','user3']
    return(
          BF.container(
              children=BF.form(children=
                    BF.textInput(label="Form Name",attr='required')+
                    BF.list(label="User Name",attr='',children=childlist)+
                    BF.fieldsetContainer(label="Permissions",children=BF.checkbox(label="Read")+BF.checkbox(label="Write"))+
                    BF.list(label="Tables",attr='multiple',children=tablelist)+
                    BF.textInput(label="Description",attr='')+
                    BF.button(label="Submit",attr='hx-post="/main/form_setup" hx-target="#mainform" hx-swap="innerHTML"')+
                    BF.button(label="Cancel",attr='onclick=document.getElementById("modal").style.display="none";')
                    ),attr='style="display:block;"',cssclass="w3-third w3-display-middle")
         )

def fieldConfig():
    return(BF.container(children=BF.form(
            children=BF.textInput(label="Field Name",attr='required')+
                BF.textInput(label="Variable Name")+
                BF.checkbox(label="Disabled")+
                BF.list(label="Table Row")+
                BF.list(label="Table Column")+
                BF.button(label="Submit",attr='hx-post="/main/add_field" hx-target="#mainform" hx-swap="innerHTML"')+
                BF.button(label="Cancel",attr='onclick=document.getElementById("modalView").style.display="none"')),
                label="Field Config",attr='style="display:block"')
    )

