from django.core import validators
from django.core.exceptions import ValidationError
from django import forms

class ValidateCustomField():
    # get custom  definition
    pass

class ValidatorInstances():

    def email(field):
        emailval=validators.EmailValidator("not an email")
        emailval(field)

    def text(field,maxlen):
        textval=validators.RegexValidator("[A-z][a-z]","can only enter text")
        lengthmax=validators.MaxLengthValidator(maxlen,"should only have 14 char")
        textval(field)
        lengthmax(field)

    def phoneno(field):
        message = "not 10 nos"
        minno=validators.MinLengthValidator(10,message)
        maxno=validators.MaxLengthValidator(10,message)
        minno(field)
        maxno(field)

    def file(field):
        fileval=validators.FileExtensionValidator("not the correct file extension")
        fileval(field)

    def password(field):
        specialchar=validators.RegexValidator("[! @#\(\)%^&]","password should contain")
        lengthmin=validators.MinLengthValidator(8,"should contain at least 8 char")
        lengthmax=validators.MaxLengthValidator(14,"should only have 14 char")
        Asciigroups=validators.RegexValidator("[A-Z][0-9]","should contain a capital letter and number")
        specialChar(field)
        lengthmin(field)
        lengthmax(field)
        Asciigroups(field)

    # validate the field based on the fieldname.fieldvalidationtype
    # if valid do nothing 
    # if invalid throw error 

