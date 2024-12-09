from django.core import validators
from django.core.exceptions import ValidationError
from django import forms
import . import BaseForm as bf

class ValidateCustomField(data)
    # get custom  definition
    pass

class ValidatorInstances(field): 

    if(field == email):
        emailval=validators.validateEmail("not an email")
        emailval(field)

    if(field == text):
        textval=validators.validateSlug("can only enter text")
        textcal(field)

    if(field == phoneno):
        message = "not 10 nos"
        minno=validators.MinLengthValidator(10,message)
        maxno=validators.MaxLengthValidator(10,message)
        minno(field)
        maxno(field)

    if (field == file):
        fileval=validators.FileExtensionValidator("not the correct file extension")
        fileval(field)

    if (field == password):
        specialchar=validators.RegexValidator(regex=,"password should contain")
        lengthmin=validators.MinLengthValidator(8,"should contain at least 8 char")
        lengthmax=validators.MaxLengthValidator(14,"should only have 14 char")
        Asciigroups=validators.RegexValidator(regex=,"should contain a capital letter and number")
        specialChar(field)
        lengthmin(field)
        lengthmax(field)
        Asciigroups(field)

    # validate the field based on the fieldname.fieldvalidationtype
    # if valid do nothing 
    # if invalid throw error 

