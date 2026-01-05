from django.db import models
from django.contrib.auth.base_user import (
    BaseUserManager,
    AbstractBaseUser,
)
from django.contrib.auth.models import PermissionsMixin
import logging
from django.contrib.auth.models import Permission, Group
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
import json
import hashlib

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
    """
    store nested table metadata

    Attributes:
        table_metadata (JSONField): store record as json string
        table_unique (bool): stores if Table data should be unique
        table_name (ForeignKey): relates TableMetaData to TableName
        created_at (DateTimeField): stores date time value of record entry 
        updated_at (DateTimeField): store date time value of record update
    """
    table_metadata = models.JSONField(encoder=DjangoJSONEncoder,
                                      null=True, blank=True, default=dict, unique=True, verbose_name="table metadata")
    table_unique = models.BooleanField(null=True)
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
    """
    This model stores the nested table data

    Attributes:
        table_data (json): stores the data in a json string
        json_hash (char): stores the has of table_data field
        table_name (ForeignKey): relates tabledata to table name
        company (ForeignKey): relates tabledata to company
        created_at (DateTimeField): stores date and time of record entry 
        updated_at (DateTimeField): stores date and time of record update
    """
    table_data = models.JSONField(encoder=DjangoJSONEncoder,
                                  null=True, blank=True, default=dict, verbose_name="table data")
    json_hash = models.CharField(
        max_length=64, editable=False, db_index=True, null=True)
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
        indexes = [GinIndex(fields=["table_data"],
                            name="table_data_gin_idx")]

    def is_unique(self) -> bool:
        """
        this checks for the table_unique flag in TableMetaData

        :return: returns the boolean value of the flag
        """
        metadata = TableMetaData.objects.get(table_name=self.table_name)
        return metadata.table_unique

    def save(self, *args, **kwargs):
        """
        overriding the save method to include hashing and unique flag check 
        to determine if the table_data has to be checked for uniqueness

        :raises ValidationError: raises validation error id duplicate data exists
        """
        normalized = json.dumps(self.table_data, sort_keys=True)
        self.json_hash = hashlib.sha256(normalized.encode('utf-8')).hexdigest()

        if self.is_unique():
            # check for duplicates
            duplicate_exists = TableData.objects.filter(
                json_hash=self.json_hash,
                table_name=self.table_name,
                company=self.company
            ).exclude(pk=self.pk).exists()
            if duplicate_exists:
                raise ValidationError(
                    "Duplicate entry not allowed in this table.")
        super().save(*args, **kwargs)


class CustomUserManager(BaseUserManager):
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
    report_data = models.JSONField(encoder=DjangoJSONEncoder, null=True)
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
