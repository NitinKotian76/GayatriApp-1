from django.db import models
from django.contrib.auth.base_user import (
    BaseUserManager,
    AbstractBaseUser
)
from django.contrib.auth.models import PermissionsMixin
import logging
from django.contrib.auth.models import Permission, Group
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
import uuid
import json
import hashlib

logger = logging.getLogger(__name__)
# Create your models here.

# ====================== Phase 2 models =======================================


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
                company=self.company,
            ).exclude(pk=self.pk).exists()
            if duplicate_exists:
                raise ValidationError(
                    "Duplicate entry not allowed in this table.")
        super().save(*args, **kwargs)


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
            ("access_form", "can access form")
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


# =========================User models here =========================


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
            **extrafields,
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
            **extrafields,
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
        verbose_name="Employee Code",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        related_name="users",
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
            models.Index(fields=['email'])
        ]

    def __str__(self):
        return self.user_emp_code

# ========================= Millsoft models Phase 1============================


class MAgent(models.Model):
    AgentId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, null=False)
    Agentname = models.CharField(null=True, max_length=100)
    Bname = models.CharField(null=True, max_length=250)
    Area = models.CharField(null=True, max_length=30)
    Road = models.CharField(null=True, max_length=30)
    City = models.CharField(null=True, max_length=30)
    Pin = models.CharField(null=True, max_length=50)
    State = models.CharField(null=True, max_length=50)
    Phone = models.CharField(null=True, max_length=50)
    Cell = models.CharField(null=True, max_length=50)
    range = models.CharField(null=True, max_length=50)
    division = models.CharField(null=True, max_length=50)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.Agentname


class MCategory(models.Model):
    CatID = models.UUIDField(null=False, primary_key=True,
                             default=uuid.uuid4, editable=False)
    Cat = models.CharField(null=True, max_length=50)
    opening = models.FloatField(null=True)
    unit = models.CharField(null=True, max_length=10)
    chap = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.Cat

# class MCompany(models.Model):
    # Compaid = models.UUIDField(
    #     null=False, primary_key=True, default=uuid.uuid4, editable=False)
    # Companyname = models.CharField(null=True, max_length=50)
    # Add = models.CharField(null=True, max_length=250)
    # Line1 = models.CharField(null=True, max_length=50)
    # Line2 = models.CharField(null=True, max_length=50)
    # Line3 = models.CharField(null=True, max_length=50)
    # Line4 = models.CharField(null=True, max_length=50)
    # HOLine1 = models.CharField(null=True, max_length=50)
    # HOLine2 = models.CharField(null=True, max_length=50)
    # HOLine3 = models.CharField(null=True, max_length=50)
    # HOLine4 = models.CharField(null=True, max_length=50)
    # district = models.CharField(null=True, max_length=50)
    # Tel = models.CharField(null=True, max_length=50)
    # Fax = models.CharField(null=True, max_length=50)
    # GSTNO = models.CharField(null=True, max_length=20)
    # BINNo = models.CharField(null=True, max_length=50)
    # LUTNo = models.CharField(null=True, max_length=50)
    # LUTDate = models.CharField(null=True, max_length=20)
    # InvoicePreFix = models.CharField(null=True, max_length=50)
    # IECNo = models.CharField(null=True, max_length=50)
    # PANNo = models.CharField(null=True, max_length=50)
    # Commissionerate = models.CharField(null=True, max_length=50)
    # Division = models.CharField(null=True, max_length=50)
    # Range = models.CharField(null=True, max_length=50)
    # LocationCode = models.CharField(null=True, max_length=50)
    # EXAMINATIONL1 = models.CharField(null=True, max_length=100)
    # EXAMINATIONL2 = models.CharField(null=True, max_length=100)
    # EXAMINATIONL3 = models.CharField(null=True, max_length=100)
    # EXAMINATIONL4 = models.CharField(null=True, max_length=100)
    # ChallanPreFix = models.CharField(null=True, max_length=10)


class MCustomer(models.Model):
    CustId = models.UUIDField(
        null=False, primary_key=True, default=uuid.uuid4, editable=False)
    Custcode = models.BigIntegerField(null=False)
    Custname = models.CharField(null=True, max_length=90)
    Bname = models.CharField(null=True, max_length=400)
    State = models.CharField(null=True, max_length=30)
    Road = models.CharField(null=True, max_length=30)
    City = models.CharField(null=True, max_length=50)
    GSTNo = models.CharField(null=True, max_length=30)
    PayTerms = models.CharField(null=True, max_length=50)
    Dispatchto = models.CharField(null=True, max_length=50)
    District = models.CharField(null=True, max_length=50)
    InvoiceType = models.CharField(null=True, max_length=50)
    PANNO = models.CharField(null=True, max_length=15)
    StateCode = models.CharField(null=True, max_length=10)
    GSTINNo = models.CharField(null=True, max_length=20)
    agentid = models.ForeignKey(MAgent, on_delete=models.CASCADE)
    CustTransport = models.CharField(null=True, max_length=60)

    def __str__(self):
        return self.Custname


class MEmployee(models.Model):
    EMPID = models.UUIDField(null=True, default=uuid.uuid4, editable=False)
    EmpName = models.CharField(null=True, max_length=50)
    Designation = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.EmpName


class MExportFields(models.Model):
    ExportID = models.UUIDField(null=True, default=uuid.uuid4, editable=False)
    DescriptionGoods = models.CharField(null=True, max_length=50)
    HSNo = models.CharField(null=True, max_length=50)
    Declaration = models.CharField(null=True, max_length=100)
    CompCode = models.CharField(null=True, max_length=10)
    DeclarationLine1 = models.CharField(null=True, max_length=100)
    DeclarationLine2 = models.CharField(null=True, max_length=100)
    DeclarationLine3 = models.CharField(null=True, max_length=100)
    DeclarationLine4 = models.CharField(null=True, max_length=100)
    INVBackPageHeading = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.ExportID


class MShade(models.Model):
    ShadeID = models.UUIDField(
        null=False, primary_key=True, default=uuid.uuid4, editable=False)
    ShadeCode = models.CharField(null=True, max_length=10)
    Shade = models.CharField(null=True, max_length=50)
    APICode = models.CharField(null=True, max_length=10)
    Gsm_M = models.FloatField(null=True)
    FlagGroup = models.BigIntegerField(null=True)
    BatchGroup = models.CharField(null=True, max_length=20)
    FieldGroup = models.CharField(null=True, max_length=10)
    GroupCategory = models.BigIntegerField(null=True)
    StockTrans_Y_N = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.ShadeCode


class MItem(models.Model):
    Itemid = models.UUIDField(
        null=False, primary_key=True, default=uuid.uuid4, editable=False)
    ItemCode = models.CharField(null=True, max_length=20)
    ShadeID = models.ForeignKey(
        MShade, on_delete=models.CASCADE)
    SizeD = models.CharField(null=True, max_length=10)
    GSM = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.ItemCode


class MItemCategory(models.Model):
    CatId = models.UUIDField(null=False, primary_key=True,
                             default=uuid.uuid4, editable=False)
    Cat = models.CharField(null=False, max_length=100)
    HSNCode = models.CharField(null=True, max_length=20)
    UnitID = models.ForeignKey(
        Company, on_delete=models.CASCADE)
    remarks = models.CharField(null=True, max_length=250)

    def __str__(self):
        return self.HSNCode


class MItemRate(models.Model):
    ItemRateID = models.UUIDField(null=False,
                                  primary_key=True, default=uuid.uuid4, editable=False)
    CatID = models.ForeignKey(MCategory, on_delete=models.CASCADE)
    ItemID = models.ForeignKey(MItem, on_delete=models.CASCADE)
    CustID = models.ForeignKey(MCustomer, on_delete=models.CASCADE)
    AgentID = models.ForeignKey(MAgent, on_delete=models.CASCADE)
    Rate = models.FloatField(null=False)

    def __str__(self):
        return self.Rate


class MLocation(models.Model):
    LocationID = models.UUIDField(
        null=True, default=uuid.uuid4, editable=False)
    Location = models.CharField(null=True, max_length=20)

    def __str__(self):
        return self.Location


class MPlusMinusHead(models.Model):
    HeadID = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    Head = models.CharField(null=True, max_length=50)
    Plus_Minus = models.CharField(null=True, max_length=10)
    Api = models.CharField(null=True, max_length=10)
    Ref = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.Head


class MSupplier(models.Model):
    SuppId = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    Suppname = models.CharField(null=True, max_length=100)
    Bname = models.CharField(null=True, max_length=250)
    Area = models.CharField(null=True, max_length=30)
    Road = models.CharField(null=True, max_length=30)
    City = models.CharField(null=True, max_length=30)
    Pin = models.CharField(null=True, max_length=50)
    State = models.CharField(null=True, max_length=50)
    Cell = models.CharField(null=True, max_length=50)
    SuppType = models.CharField(null=True, max_length=10)
    GSTNo = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.Suppname


class TInvoice(models.Model):
    InvoiceID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    CustID = models.ForeignKey(
        MCustomer, on_delete=models.CASCADE)
    AgentID = models.ForeignKey(
        MAgent, on_delete=models.CASCADE)
    InvoiceNo = models.BigIntegerField(null=False)
    InvoiceDate = models.DateTimeField(null=True)
    ShadeID = models.ForeignKey(
        MShade, on_delete=models.CASCADE)
    SalesType = models.CharField(null=True, max_length=20)
    PreTime = models.CharField(null=True, max_length=20)
    PreDate = models.DateTimeField(null=True)
    RemTime = models.CharField(null=True, max_length=20)
    RemDate = models.DateTimeField(null=True)
    OrderNo = models.CharField(null=True, max_length=50)
    OrderDate = models.CharField(null=True, max_length=10)
    Transport = models.CharField(null=True, max_length=90)
    VehicleNo = models.CharField(null=True, max_length=50)
    LrNo = models.CharField(null=True, max_length=50)
    LrDate = models.CharField(null=True, max_length=20)
    PayTerms = models.CharField(null=True, max_length=10)
    Remarks = models.CharField(null=True, max_length=60)
    AssValue = models.FloatField(null=True)
    Excise = models.CharField(null=True, max_length=10)
    ExciseAmt = models.FloatField(null=True)
    Cess = models.CharField(null=True, max_length=10)
    CessAmt = models.FloatField(null=True)
    Cst = models.CharField(null=True, max_length=10)
    CstAmt = models.FloatField(null=True)
    Vat = models.CharField(null=True, max_length=10)
    VatAmt = models.FloatField(null=True)
    AddVat = models.CharField(null=True, max_length=10)
    AddVatAmt = models.FloatField(null=True)
    Insurance = models.CharField(null=True, max_length=10)
    InsuranceAmt = models.FloatField(null=True)
    GTotal = models.FloatField(null=True)
    ExciseSubTotal = models.FloatField(null=True)
    VatSubTotal = models.FloatField(null=True)
    DeliveryAt = models.CharField(null=True, max_length=60)
    FlgType = models.IntegerField(null=True)
    FlgSaleType = models.IntegerField(null=True)
    InvoiceType = models.CharField(null=True, max_length=20)
    Ind_Weight = models.FloatField(null=True)
    # buttons for
    # CreateUser
    # CreateDate
    # UpdateUser
    # UpdateDate

    def __str__(self):
        return self.InvoiceNo


class TExport(models.Model):
    ExportID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    InvoiceID = models.ForeignKey(
        TInvoice, on_delete=models.CASCADE)
    PreCarriageby = models.CharField(null=True, max_length=100)
    Receiptby = models.CharField(null=True, max_length=100)
    VesselFlightNo = models.CharField(null=True, max_length=50)
    PortofLoading = models.CharField(null=True, max_length=90)
    ContainerNo = models.CharField(null=True, max_length=50)
    PortofDischarge = models.CharField(null=True, max_length=90)
    PaymentType = models.CharField(null=True, max_length=50)
    EmpNAme = models.CharField(null=True, max_length=50)
    EmpMoNo = models.CharField(null=True, max_length=50)
    DollarRate = models.FloatField(null=True)
    ExchangeRate = models.FloatField(null=True)
    DollarTotal = models.FloatField(null=True)
    ExchageTotal = models.FloatField(null=True)
    NoOfReels = models.FloatField(null=True)
    ContainerSize = models.CharField(null=True, max_length=50)
    EmptyConWeight = models.CharField(null=True, max_length=50)
    MaxConWeight = models.CharField(null=True, max_length=50)
    RFIDSealNo = models.CharField(null=True, max_length=50)
    LinerSealNo = models.CharField(null=True, max_length=50)
    BankName = models.CharField(null=True, max_length=50)
    PaymentTerms = models.CharField(null=True, max_length=50)
    ShippingBillNo = models.CharField(null=True, max_length=50)
    ShippingBillDate = models.CharField(null=True, max_length=50)
    WeighBridge = models.CharField(null=True, max_length=100)
    HSCode = models.CharField(null=True, max_length=50)
    DescriptionGoods = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.ExportID


class TExportDetails(models.Model):
    ExportDetailsID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    ExportID = models.ForeignKey(
        TExport, on_delete=models.CASCADE)
    ReelNo = models.FloatField(null=True)
    GWeight = models.FloatField(null=True)
    TareWeight = models.FloatField(null=True)
    NetWeight = models.FloatField(null=True)
    InvoiceID = models.ForeignKey(
        TInvoice, on_delete=models.CASCADE)
    # RewinderID = not there for unit 1
    Size = models.CharField(null=True, max_length=20)
    GSM = models.FloatField(null=True)
    NoOfReam_Sheets = models.FloatField(null=True)
    UOM = models.CharField(null=True, max_length=10)
    DollarRAte = models.FloatField(null=True)
    InvoiceNo = models.CharField(null=True, max_length=10)
    INvoicedate = models.DateTimeField(null=True)
    NoOFReam = models.FloatField(null=True)
    REAMWt = models.FloatField(null=True)

    def __str__(self):
        return self.ExportDetailsID


class TIndent(models.Model):
    IndentID = models.AutoField(primary_key=True)
    CustID = models.ForeignKey(
        MCustomer, on_delete=models.CASCADE)
    IndentNo = models.CharField(null=True, max_length=20)
    IndentDate = models.DateTimeField(null=True)
    PONo = models.CharField(null=True, max_length=20)
    PODate = models.DateTimeField(null=True)
    remark = models.CharField(null=True, max_length=150)

    def __str__(self):
        return self.IndentNo


class TJumboRollWiseQC(models.Model):
    JumboRollWiseQcID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    JumboRollQCDate = models.DateTimeField(null=True)
    JumboRollNo = models.DecimalField(
        null=True, max_digits=18, decimal_places=0)
    Shift = models.CharField(null=True, max_length=10)
    ShadeID = models.ForeignKey(
        MShade, on_delete=models.CASCADE)
    GSM = models.CharField(null=True, max_length=10)
    CALIPER = models.CharField(null=True, max_length=10)
    BULK_QC = models.CharField(null=True, max_length=10)
    COBBTOP = models.CharField(null=True, max_length=10)
    BOTTOM = models.CharField(null=True, max_length=10)
    MOISTUREavg = models.CharField(null=True, max_length=10)
    TABERSTIFFNESSMDCD = models.CharField(null=True, max_length=10)
    RATIO = models.CharField(null=True, max_length=10)
    BRIGHTNESS = models.CharField(null=True, max_length=10)
    GLOSS = models.CharField(null=True, max_length=10)
    SOATVALUE = models.CharField(null=True, max_length=10)
    PPSROUGHNESS = models.CharField(null=True, max_length=10)
    IGTDRYPICK = models.CharField(null=True, max_length=10)
    PLYBONDSCOTT = models.CharField(null=True, max_length=10)
    SURFACEPH = models.CharField(null=True, max_length=10)
    SURACEDUST = models.CharField(null=True, max_length=10)
    TOPFORMATION = models.CharField(null=True, max_length=10)
    VARNISHABILITY = models.CharField(null=True, max_length=10)
    CRACKINGCREASING = models.CharField(null=True, max_length=10)
    FLATNESS = models.CharField(null=True, max_length=10)
    JumboRollWeight = models.FloatField(null=True)
    DateM = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.JumboRollNo


class TLOTNoWiseQc(models.Model):
    LOTNoWiseQcID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    JumboRollWiseQcID = models.ForeignKey(
        TJumboRollWiseQC, on_delete=models.CASCADE)
    LOTNoWiseQcIDDate = models.DateTimeField(null=True)
    L_E = models.CharField(null=True, max_length=10)
    ShadeID = models.ForeignKey(MShade, on_delete=models.CASCADE)
    Reel_Sheet = models.CharField(null=True, max_length=10)
    ItemID = models.ForeignKey(MItem, on_delete=models.CASCADE)
    Length = models.CharField(null=True, max_length=10)
    UnitID = models.ForeignKey(Company, on_delete=models.CASCADE)
    CM_Inch = models.CharField(null=True, max_length=10)
    LocationID = models.ForeignKey(MLocation, on_delete=models.CASCADE)
    IndentNo = models.CharField(null=True, max_length=20)
    CustID = models.ForeignKey(MCustomer, on_delete=models.CASCADE)
    AgentID = models.ForeignKey(MAgent, on_delete=models.CASCADE)
    LotNo = models.CharField(null=True, max_length=50)
    DateM = models.CharField(null=True, max_length=10)
    LotNoDateM = models.CharField(null=True, max_length=10)
    Weight = models.FloatField(null=True)
    NoOfSheet = models.CharField(null=True, max_length=10)
    ReamWt = models.CharField(null=True, max_length=10)
    NoOfReam = models.CharField(null=True, max_length=10)
    Grain = models.CharField(null=True, max_length=10)
    FPNo = models.CharField(null=True, max_length=10)
    Sized = models.CharField(null=True, max_length=10)
    GSM = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.LotNo


class TProduction(models.Model):
    ProductionID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    RDate = models.DateTimeField(null=True)
    L_E = models.CharField(null=True, max_length=10)
    CatID = models.ForeignKey(MCategory, on_delete=models.CASCADE)
    ShadeID = models.ForeignKey(MShade, on_delete=models.CASCADE)
    Reel_Sheet = models.CharField(null=True, max_length=50)
    ItemID = models.ForeignKey(MItem, on_delete=models.CASCADE)
    Length = models.CharField(null=True, max_length=10)
    UnitID = models.ForeignKey(Company, on_delete=models.CASCADE)
    ReelNoFrom = models.BigIntegerField(null=False)
    ReelNoTO = models.BigIntegerField(null=True)
    NoOfSheet = models.BigIntegerField(null=True)
    NoOfBDLS = models.FloatField(null=True)
    NoOfREAM = models.FloatField(null=True)
    REAMWt = models.FloatField(null=True)
    Weight = models.FloatField(null=True)
    Rate = models.FloatField(null=True)
    LocationID = models.ForeignKey(MLocation, on_delete=models.CASCADE)
    IndentNo = models.CharField(null=True, max_length=20)
    CustID = models.ForeignKey(MCustomer, on_delete=models.CASCADE)
    AgentID = models.ForeignKey(MAgent, on_delete=models.CASCADE)
    OBFlag = models.IntegerField(null=True)
    APIFlag = models.CharField(null=True, max_length=10)
    FAC = models.CharField(null=True, max_length=10)
    Stk = models.CharField(null=True, max_length=10)
    Approved = models.BigIntegerField(null=True)
    EntryType = models.CharField(null=True, max_length=20)
    StockPlus_Minus = models.CharField(null=True, max_length=10)
    HeadId = models.BigIntegerField(null=True)
    # for remaining stock removal from inventory
    RefProductionid = models.UUIDField(null=True)
    P_M_Remarks = models.CharField(null=True, max_length=60)
    Ind_Weight = models.FloatField(null=True)
    CM_Inch = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.ProductionID


class TProduction_bck(models.Model):
    ProductionID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    RDate = models.DateTimeField(null=True)
    L_E = models.CharField(null=True, max_length=10)
    CatID = models.ForeignKey(MCategory, on_delete=models.CASCADE)
    ShadeID = models.ForeignKey(MShade, on_delete=models.CASCADE)
    Reel_Sheet = models.CharField(null=True, max_length=50)
    ItemID = models.ForeignKey(MItem, on_delete=models.CASCADE)
    Length = models.CharField(null=True, max_length=10)
    UnitID = models.ForeignKey(Company, on_delete=models.CASCADE)
    ReelNoFrom = models.BigIntegerField(null=False)
    ReelNoTO = models.BigIntegerField(null=True)
    NoOfSheet = models.BigIntegerField(null=True)
    NoOfBDLS = models.FloatField(null=True)
    NoOfREAM = models.FloatField(null=True)
    REAMWt = models.FloatField(null=True)
    Weight = models.FloatField(null=True)
    Rate = models.FloatField(null=True)
    LocationID = models.ForeignKey(MLocation, on_delete=models.CASCADE)
    IndentNo = models.CharField(null=True, max_length=20)
    CustID = models.ForeignKey(MCustomer, on_delete=models.CASCADE)
    AgentID = models.ForeignKey(MAgent, on_delete=models.CASCADE)
    OBFlag = models.IntegerField(null=True)
    APIFlag = models.CharField(null=True, max_length=10)
    FAC = models.CharField(null=True, max_length=10)
    Stk = models.CharField(null=True, max_length=10)
    Approved = models.BigIntegerField(null=True)
    EntryType = models.CharField(null=True, max_length=20)
    StockPlus_Minus = models.CharField(null=True, max_length=10)
    HeadId = models.BigIntegerField(null=True)
    RefProductionid = models.UUIDField(null=True)
    P_M_Remarks = models.CharField(null=True, max_length=60)

    Ind_Weight = models.FloatField(null=True)
    CM_Inch = models.CharField(null=True, max_length=10)


class TProductionReel(models.Model):
    ProductionReelID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    ProductionID = models.ForeignKey(TProduction, on_delete=models.CASCADE)
    ReelNo = models.BigIntegerField(null=True)
    Stk = models.CharField(null=True, max_length=10)
    StkDate = models.DateTimeField(null=True)
    InvDate = models.DateTimeField(null=True)
    RefProductionReelid = models.UUIDField(null=True)


class RChallan(models.Model):
    Custname = models.CharField(null=True, max_length=100)
    Bname = models.CharField(null=True, max_length=100)
    City = models.CharField(null=True, max_length=20)
    State = models.CharField(null=True, max_length=20)
    StateCode = models.CharField(null=True, max_length=10)
    PANNO = models.CharField(null=True, max_length=10)
    GSTINNo = models.CharField(null=True, max_length=20)
    InvoiceNo = models.CharField(null=True, max_length=10)
    InvoiceDate = models.DateTimeField(null=True)
    OrderNo = models.CharField(null=True, max_length=50)
    OrderDate = models.CharField(null=True, max_length=10)
    Dispatchto = models.CharField(null=True, max_length=100)
    LrNo = models.CharField(null=True, max_length=50)
    LrDate = models.CharField(null=True, max_length=10)
    VehicleNo = models.CharField(null=True, max_length=100)
    Transport = models.CharField(null=True, max_length=100)
    Quality = models.CharField(null=True, max_length=20)
    Shade = models.CharField(null=True, max_length=20)
    GSM = models.CharField(null=True, max_length=10)
    lENGTH = models.FloatField(null=True)
    Sized = models.FloatField(null=True)
    Unit = models.CharField(null=True, max_length=10)
    InvoiceID = models.ForeignKey(TInvoice, on_delete=models.CASCADE)
    NoOfSheet = models.FloatField(null=True)
    REAMWt = models.FloatField(null=True)
    NoOfREAM = models.FloatField(null=True)
    NoOfBDLS = models.FloatField(null=True)
    BDLS = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    REmarks = models.CharField(null=True, max_length=100)


class RChallanExport(models.Model):

    Custname = models.CharField(null=True, max_length=100),
    Bname = models.CharField(null=True, max_length=100),
    City = models.CharField(null=True, max_length=50)
    State = models.CharField(null=True, max_length=20)
    StateCode = models.CharField(null=True, max_length=10)
    PANNO = models.CharField(null=True, max_length=10)
    GSTINNo = models.CharField(null=True, max_length=20)
    InvoiceNo = models.CharField(null=True, max_length=10)
    InvoiceDate = models.DateTimeField(null=True)
    OrderNo = models.CharField(null=True, max_length=20)
    OrderDate = models.CharField(null=True, max_length=10)
    Dispatchto = models.CharField(null=True, max_length=100)
    LrNo = models.CharField(null=True, max_length=50)
    LrDate = models.CharField(null=True, max_length=10)
    VehicleNo = models.CharField(null=True, max_length=100),
    Transport = models.CharField(null=True, max_length=100),
    Quality = models.CharField(null=True, max_length=20)
    Shade = models.CharField(null=True, max_length=20)
    GSM = models.CharField(null=True, max_length=10)
    lENGTH = models.FloatField(null=True)
    Sized = models.FloatField(null=True)
    Unit = models.CharField(null=True, max_length=10)
    InvoiceID = models.ForeignKey(TInvoice, on_delete=models.CASCADE)
    NoOfSheet = models.FloatField(null=True)
    REAMWt = models.FloatField(null=True)
    NoOfREAM = models.FloatField(null=True)
    NoOfBDLS = models.FloatField(null=True)
    BDLS = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    REmarks = models.CharField(null=True, max_length=100),
    ReelNo = models.BigIntegerField(null=True)
    ProductionReelID = models.ForeignKey(
        TProductionReel, on_delete=models.CASCADE)
    ProductionID = models.ForeignKey(TProduction, on_delete=models.CASCADE)
    Reel_Sheet = models.CharField(null=True, max_length=50)
