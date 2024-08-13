from django.db import models

# Create your models here.
class Profile(models.Model):
    userName= models.CharField()
    userPass= models.CharField()

class AdminProfile(models.Model):
    AdminName= models.CharField()
