from django.core import validators
from django import forms

class customValidateField(forms.Field)
    #  custom validate the form value #
    #__________________________#

    def to_python(self,value):
        if not value:
            return []
        return value.split(",")

    def validate(self,value):
        super().validate(value)
        for email in value:
            validators.validate_email(email)

class ValidateFields(fieldName):
    # validate the field based on the fieldname.fieldvalidationtype
    # if valid do nothing 
    # if invalid throw error 

