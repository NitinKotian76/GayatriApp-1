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
    company_name = models.CharField( max_length=255,null=True, verbose_name="company name") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.company_name


class TableName(models.Model):
    table_name = models.CharField(max_length=255,null=True, blank=True,verbose_name="table name")  
    company = models.ForeignKey(Company, on_delete=models.CASCADE , related_name="tables")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        constraints = [models.UniqueConstraint(
            fields=["table_name", "company"], name="unique_table_name_company")]
        # IMPROVEMENT NEEDED: Add ordering and indexes for frequently queried fields

    def __str__(self):
        return self.table_name


class TableData(models.Model):
    # IMPROVEMENT NEEDED: Add proper validation for JSONField
    # IMPROVEMENT NEEDED: Add related_name for ForeignKeys
    table_data = models.JSONField(
        null=True, blank=True, default=dict, unique=True, verbose_name="table data")
    table_name = models.ForeignKey(TableName, on_delete=models.CASCADE , related_name="data_rows")  # Should add: related_name="data_rows"
    company = models.ForeignKey(Company, on_delete=models.CASCADE , related_name="table_data")  # Should add: related_name="table_data"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        constraints = [models.UniqueConstraint(
            fields=["table_data", "table_name", "company"], name="unique_table_data_table_name_company")]
        indexes = [GinIndex(fields=["table_data"], name="table_data_gin_idx")]


class CustomUserManager(BaseUserManager):
    # IMPROVEMENT NEEDED: Add proper error messages for validation
    # IMPROVEMENT NEEDED: Add email validation in create_user
    def create_user(self, user_emp_code, password=None):
        if not user_emp_code:
            raise ValueError("user must have emp code")

        user = self.model(
            email=self.normalize_email(email),
            user_emp_code=user_emp_code,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_emp_code, password=None):
        # IMPROVEMENT NEEDED: Add proper validation for superuser creation
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
    user_name = models.CharField(max_length=255, verbose_name="User Name")
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
    )
    user_emp_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Employee Code"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        related_name="users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "user_emp_code"
    REQUIRED_FIELDS = ["email", "user_name"]

    objects = CustomUserManager()
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_emp_code']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.user_emp_code


class Form(models.Model):
    # IMPROVEMENT NEEDED: Add proper field constraints and validations
    # IMPROVEMENT NEEDED: Add proper verbose_names
    logger.debug("form added")
    form_name = models.CharField()  # Should be: models.CharField(max_length=255, verbose_name="Form Name")
    group = models.ManyToManyField(Group)  # Should add: related_name="forms"
    table = models.ManyToManyField(TableName)  # Should add: related_name="forms"
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Should add: related_name="forms"

    form_data = models.JSONField(null=True)  # IMPROVEMENT NEEDED: Add proper validation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("edit_form", "can edit form"),
            ("access_form", "can access form"),
        ]
        # IMPROVEMENT NEEDED: Add proper ordering and indexes


class Report(models.Model):
    # IMPROVEMENT NEEDED: Add proper field constraints and validations
    # IMPROVEMENT NEEDED: Add proper verbose_names
    report_name = models.CharField()  # Should be: models.CharField(max_length=255, verbose_name="Report Name")
    report_data = models.JSONField(null=True)  # IMPROVEMENT NEEDED: Add proper validation
    group = models.ManyToManyField(Group)  # Should add: related_name="reports"
    table = models.ManyToManyField(TableName)  # Should add: related_name="reports"
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Should add: related_name="reports"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # IMPROVEMENT NEEDED: Add proper ordering and indexes
        pass
