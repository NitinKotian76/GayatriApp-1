from django.db import models

# Create your models here.
class Profile(models.Model):
    userName= models.CharField()
    userForms=models.JSONField()

class AdminProfile(models.Model):
    AdminName= models.CharField()
    AdminDraftForms= models.JSONField()
