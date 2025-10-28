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
    company_name = models.CharField(
        max_length=255, null=True, verbose_name="company name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.company_name


class TableName(models.Model):
    table_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="table name")
    description = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="table description")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="tables")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        constraints = [models.UniqueConstraint(
            fields=["table_name", "company"], name="unique_table_name_company")]
        # IMPROVEMENT NEEDED: Add ordering and indexes for frequently queried fields

    def __str__(self):
        return self.table_name


class TableMetaData(models.Model):
    # IMPROVEMENT NEEDED: Add proper validation for JSONField
    # IMPROVEMENT NEEDED: Add related_name for ForeignKeys
    table_metadata = models.JSONField(
        null=True, blank=True, default=dict, unique=True, verbose_name="table metadata")
    table_name = models.ForeignKey(
        TableName, on_delete=models.CASCADE, related_name="metadata")
    # Should add: related_name="table_data"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        constraints = [models.UniqueConstraint(
            fields=["table_metadata", "table_name"], name="unique_table_metadata_name")]
        indexes = [GinIndex(fields=["table_metadata"],
                            name="table_metadata_gin_idx")]


class TableData(models.Model):
    # IMPROVEMENT NEEDED: Add proper validation for JSONField
    # IMPROVEMENT NEEDED: Add related_name for ForeignKeys

    table_data = models.JSONField(
        null=True, blank=True, default=dict, unique=True, verbose_name="table data")
    # Should add: related_name="data_rows"
    table_name = models.ForeignKey(
        TableName, on_delete=models.CASCADE, related_name="data_rows")
    # Should add: related_name="table_data"
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="table_data")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']
        constraints = [models.UniqueConstraint(
            fields=["table_data", "table_name", "company"], name="unique_table_data_name_company")]
        indexes = [GinIndex(fields=["table_data"],
                            name="table_data_gin_idx")]


class CustomUserManager(BaseUserManager):
    # IMPROVEMENT NEEDED: Add proper error messages for validation
    # IMPROVEMENT NEEDED: Add email validation in create_user
    def create_user(self, email, user_name, user_emp_code, password=None, **extrafields):
        if not user_emp_code:
            raise ValueError("user must have emp code")
        if not email:
            raise ValueError("user must have an email")

        user = self.model(
            user_name=user_name,
            email=self.normalize_email(email),
            user_emp_code=user_emp_code,
            **extrafields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, user_emp_code, password=None, **extrafields):
        # IMPROVEMENT NEEDED: Add proper validation for superuser creation
        extrafields.setdefault('is_admin', True)
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)

        return self.create_user(
            email,
            user_name,
            user_emp_code=user_emp_code,
            password=password,
            **extrafields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=50, verbose_name="User Name")
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
    # Should be: models.CharField(max_length=255, verbose_name="Form Name")
    form_name = models.CharField()
    group = models.ManyToManyField(Group)  # Should add: related_name="forms"
    # Should add: related_name="forms"
    table = models.ManyToManyField(TableName)
    # Should add: related_name="forms"
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # IMPROVEMENT NEEDED: Add proper validation
    form_data = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Form"
        verbose_name_plural = "Forms"
        ordering = ['-created_at']
        permissions = [
            ("edit_form", "can edit form"),
            ("access_form", "can access form"),
        ]
        # IMPROVEMENT NEEDED: Add proper ordering and indexes


class Report(models.Model):
    # IMPROVEMENT NEEDED: Add proper field constraints and validations
    # IMPROVEMENT NEEDED: Add proper verbose_names
    # Should be: models.CharField(max_length=255, verbose_name="Report Name")
    report_name = models.CharField()
    # IMPROVEMENT NEEDED: Add proper validation
    report_data = models.JSONField(null=True)
    group = models.ManyToManyField(Group)  # Should add: related_name="reports"
    # Should add: related_name="reports"
    table = models.ManyToManyField(TableName)
    # Should add: related_name="reports"
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ['-created_at']


class Template(models.Model):
    template_name = models.CharField()
    file_type = models.CharField()
    file_data = models.FileField(upload_to="ReportTemplates/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"
        ordering = ['-created_at']
