from . import BaseForm as bf 

class formFieldData():

 def addFields():
    pass 
 def removeFields():

  pass

 def changeFields():
  pass

 def modifyAccess():
  pass

 def saveForm():
  # form.write(json.dumps(fieldData))
  pass 

 def saveDraft(*args, **kwargs):
  #dictionary data for the draft
  formdata = Kwargs.get()
 
  # draftFormData= { "field1": {
  #                 "fieldType": "textInput",
  #                 "fieldLabel": "label",
  #                 "attributes": {
  #                     "disabled": true,
  #                     "autocomplete": true,
  #                     }, 
  #                 "tableVar": "table1",
  #                 "VarName": "fieldvar"
  #           }
  return draftFormData

 def deleteDraft():
  pass
