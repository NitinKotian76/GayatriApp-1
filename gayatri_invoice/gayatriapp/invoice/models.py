from django.db import models
from django.contrib.auth.base_user import (
    BaseUserManager,
    AbstractBaseUser,
)
from django.contrib.auth.models import PermissionsMixin
import logging
from django.contrib.auth.models import Permission, Group
from django.contrib.postgres.indexes import GinIndex

logger = logging.getLogger(__name__)
# Create your models here.


class Company(models.Model):
    # user based
    company_name = models.CharField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class TableName(models.Model):
    table_name = models.CharField(unique=True, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.table_name


class TableData(models.Model):
    table_data = models.JSONField(
        null=True, blank=True, default=dict, unique=True)
    table_name = models.ForeignKey(TableName, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [GinIndex(fields=["table_data"], name="table_data_gin_idx")]


class CustomUserManager(BaseUserManager):
    def create_user(self, user_emp_code, password=None):

        if not user_emp_code:
            raise ValueError("user must have emp code")

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "user_emp_code"
    REQUIRED_FIELD = []

    objects = CustomUserManager()
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user_emp_code


class Form(models.Model):
    logger.debug("form added")
    form_name = models.CharField()
    group = models.ManyToManyField(Group)
    table = models.ManyToManyField(TableName)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    form_data = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("edit_form", "can edit form"),
            ("access_form", "can access form"),
        ]


class Report(models.Model):
    report_name = models.CharField()
    report_data = models.JSONField(null=True)
    group = models.ManyToManyField(Group)
    table = models.ManyToManyField(TableName)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
