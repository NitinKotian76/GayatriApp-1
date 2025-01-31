from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
# Create your models here.


class UserProfile(AbstractBaseUser):
    logger.debug("entry added")
    username = models.CharField()
    email = models.EmailField("email address")
    userCompany = models.CharField()
    userLog = models.JSONField(null=True)
    userAccess = models.JSONField(null=True)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username", "userCompany"]
    
    class Meta:
        permissions = [
                ("can create user"),
                ("can edit user"),
                ("can delete user"),
                ("can set is_active"),
                ]

    def create_user(self, username, email, userCompany, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not userCompany:
            raise ValueError("User must have a userCompany")
        user = self.model(
                username=username,
                email=self.normalize_email(email),
                userCompany=userCompany,
                )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, userCompany, password=None):
        user = self.create_user( 
                                email,
                                password=password,
                                username=username,
                                userCompany=userCompany,
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Form(models.Model):
    logger.debug("form added")
    formName = models.CharField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    formData = models.JSONField(null=True)
    class Meta:
        permissions = [
                ("edit form","can edit form"),
                ("delete form","can delete form"),
                ("access form","can access form"),
                ]


# class Table(models.Model):
#     logger.debug("table added")
#     TableName = models.CharField()
#     TableData = models.JSONField()
#     TablePermission = models.JSONField(null=True)
