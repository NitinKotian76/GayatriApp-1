from django.db import models
from dynamic_models.models import ModelSchema, FieldSchema
from django.contrib.postgres.fields import ArrayField
import uuid

# Create your models here.
class UserProfile(models.Model):
    userName= models.CharField()
    userPass= models.CharField()

class Forms(models.Model):
    """ 
        just add and proccess the forms in their json form so dont have to implement
        Dynamic forms which can get messy
    """
    formName = models.CharField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hasAccess = ArrayField(models.CharField())

class Dynamic_models():
    def __init__(Modelname,Fields):
        self.modelName = ModelName
        self.Fields = Fields

    def create_model():
        data= ModelSchema.objects.create(name=modelName)

    def create_fields():
        # use the array to make the field schema
        # data = FieldSchema.objects.create(array[])
        pass

    def populate_fields():
        # data.objects.create(values from form)
        pass

    def delete_model(): # drops the table
        pass

    def delete_field(): # drops the column
        pass

