from django.db import models
from django.contrib.auth.base_user import (
    BaseUserManager,
    AbstractBaseUser,
)
from django.contrib.auth.models import PermissionsMixin
import logging
from django.contrib.auth.models import Permission, Group
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.fields import ArrayField, JSONField

logger = logging.getLogger(__name__)
# Create your models here.


<<<<<<< HEAD
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
=======
class Company(models.Model):
    # user based
    company_name = models.CharField(null=True)

    def __str__(self):
        return self.company_name


class Table(models.Model):
    logger.debug("table added")
    # modified time
    table_name = models.CharField(unique=True)
    table_data = models.JSONField(null=True, blank=True, default=dict)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        indexes = [GinIndex(fields=["table_data"], name="table_data_gin_idx")]

    def __str__(self):
        return self.table_name


class CustomUserManager(BaseUserManager):
    def create_user(self, user_emp_code, password=None):

        if not user_emp_code:
            raise ValueError("user must have emp code")
>>>>>>> develop

        user = self.model(
            # email=self.normalize_email(email),
            user_emp_code=user_emp_code,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_emp_code, password=None):

        user = self.create_user(
            # email,
            user_emp_code=user_emp_code,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    logger.debug("entry added")
    user_name = models.CharField()
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
    )
    user_emp_code = models.CharField(unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    group = models.ManyToManyField(Group)
    USERNAME_FIELD = "user_emp_code"
    REQUIRED_FIELD = []

    objects = CustomUserManager()
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user_emp_code

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm, obj=None):
        if self.is_superuser == True and self.is_active == True:
            return True

    def has_module_perms(self, app_label):
        return True

    def get_group_permission(self, obj=None):
        return Permission.objects.filter(name="user_emp_code")

    def get_all_permissions(sel, obj=None):
        return Permission.objects.all()


class Form(models.Model):
    logger.debug("form added")
    form_name = models.CharField()
    group = models.ManyToManyField(Group)
    table = models.ManyToManyField(Table)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    form_data = models.JSONField(null=True)
    # modified time

    class Meta:
        permissions = [
            ("edit_form", "can edit form"),
            ("access_form", "can access form"),
        ]


class Report(models.Model):
    report_name = models.CharField()
    report_data = models.JSONField(null=True)
    group = models.ManyToManyField(Group)
    table = models.ManyToManyField(Table)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.report_name
