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

from django.db.utils import settings

logger = logging.getLogger(__name__)
# Create your models here


class Audit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                   blank=True, on_delete=models.SET_NULL, editable=False,
                                   related_name="%(class)s_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                   blank=True, on_delete=models.SET_NULL, editable=False,
                                   related_name="%(class)s_updated")

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']

        indexes = [
            models.Index(fields=['created_by']),
            models.Index(fields=['updated_by']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

# ====================== Phase 2 models =======================================


class Company(Audit):
    # user based
    company_name = models.CharField(
        max_length=255, null=True, verbose_name="company name")
    add = models.CharField(null=True, max_length=250, blank=True)
    line1 = models.CharField(null=True, max_length=50, blank=True)
    line2 = models.CharField(null=True, max_length=50, blank=True)
    line3 = models.CharField(null=True, max_length=50, blank=True)
    line4 = models.CharField(null=True, max_length=50, blank=True)
    holine1 = models.CharField(null=True, max_length=50, blank=True)
    holine2 = models.CharField(null=True, max_length=50, blank=True)
    holine3 = models.CharField(null=True, max_length=50, blank=True)
    holine4 = models.CharField(null=True, max_length=50, blank=True)
    district = models.CharField(null=True, max_length=50, blank=True)
    tel = models.CharField(null=True, max_length=50, blank=True)
    fax = models.CharField(null=True, max_length=50, blank=True)
    gstno = models.CharField(null=True, max_length=20, blank=True)
    binno = models.CharField(null=True, max_length=50, blank=True)
    lutno = models.CharField(null=True, max_length=50, blank=True)
    lutdate = models.CharField(null=True, max_length=20, blank=True)
    invoiceprefix = models.CharField(null=True, max_length=50, blank=True)
    iecno = models.CharField(null=True, max_length=50, blank=True)
    panno = models.CharField(null=True, max_length=50, blank=True)
    commissionerate = models.CharField(null=True, max_length=50, blank=True)
    division = models.CharField(null=True, max_length=50, blank=True)
    range = models.CharField(null=True, max_length=50, blank=True)
    location_code = models.CharField(null=True, max_length=50, blank=True)
    examinationl1 = models.CharField(null=True, max_length=100, blank=True)
    examinationl2 = models.CharField(null=True, max_length=100, blank=True)
    examinationl3 = models.CharField(null=True, max_length=100, blank=True)
    examinationl4 = models.CharField(null=True, max_length=100, blank=True)
    challanprefix = models.CharField(null=True, max_length=10, blank=True)

    def __str__(self):
        return self.company_name


class TableName(Audit):
    table_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="table name")
    description = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="table description")
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, related_name="tables")

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["table_name", "company"], name="unique_table_name_company")]

    def __str__(self):
        return self.table_name


class TableMetaData(Audit):
    """
    store nested table metadata

    Attributes:
        table_metadata (JSONField): store record as json string
        table_unique (bool): stores if Table data should be unique
        table_name (ForeignKey): relates TableMetaData to TableName
        created_at (DateTimeField): stores date time value of record entry
        updated_at (DateTimeField): store date time value of record update
    """
    table_metadata = models.JSONField(encoder=DjangoJSONEncoder, null=True,
                                      blank=True, default=dict, unique=True,
                                      verbose_name="table metadata")
    table_unique = models.BooleanField(null=True)
    table_name = models.ForeignKey(
        TableName, on_delete=models.SET_NULL, null=True, related_name="metadata")
    # Should add: related_name="table_data"

    class Meta(Audit.Meta):
        constraints = [models.UniqueConstraint(
            fields=["table_metadata", "table_name"], name="unique_table_metadata_name")]
        indexes = Audit.Meta.indexes+[GinIndex(fields=["table_metadata"],
                                               name="table_metadata_gin_idx")]


class TableData(Audit):
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
        TableName, on_delete=models.SET_NULL, null=True, related_name="data_rows")
    # Should add: related_name="table_data"
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, related_name="table_data")

    class Meta(Audit.Meta):
        indexes = Audit.Meta.indexes+[GinIndex(fields=["table_data"],
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


class Form(Audit):
    # IMPROVEMENT NEEDED: Add proper field constraints and validations
    # IMPROVEMENT NEEDED: Add proper verbose_names
    logger.debug("form added")
    # Should be: models.CharField(max_length=255, verbose_name="Form Name")
    form_name = models.CharField()
    group = models.ManyToManyField(Group)  # Should add: related_name="forms"
    # Should add: related_name="forms"
    table = models.ManyToManyField(TableName)
    # Should add: related_name="forms"
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

    # IMPROVEMENT NEEDED: Add proper validation
    form_data = models.JSONField(null=True)

    class Meta(Audit.Meta):
        permissions = [
            ("edit_form", "can edit form"),
            ("access_form", "can access form")
        ]
        # IMPROVEMENT NEEDED: Add proper ordering and indexes


class Report(Audit):
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
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)


class Template(Audit):
    template_name = models.CharField()
    file_type = models.CharField()
    file_data = models.FileField(upload_to="ReportTemplates/")

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
        on_delete=models.SET_NULL, null=True,
        related_name="users",
    )

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
        indexes = [
            models.Index(fields=['user_emp_code']),
            models.Index(fields=['email'])
        ]

    def __str__(self):
        return self.user_emp_code

# ========================= Millsoft models Phase 1============================


class MAgent(Audit):
    agentid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, null=False, editable=False)
    agentname = models.CharField(null=True, max_length=100)
    bname = models.CharField(null=True, max_length=250)
    area = models.CharField(null=True, max_length=30)
    road = models.CharField(null=True, max_length=30)
    city = models.CharField(null=True, max_length=30)
    pin = models.CharField(null=True, max_length=50)
    state = models.CharField(null=True, max_length=50)
    phone = models.CharField(null=True, max_length=50)
    cell = models.CharField(null=True, max_length=50)
    range = models.CharField(null=True, max_length=50)
    division = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.agentname


class MCategory(Audit):
    catid = models.UUIDField(null=False, primary_key=True,
                             default=uuid.uuid4, editable=False)
    cat = models.CharField(null=True, max_length=50)
    opening = models.FloatField(null=True)
    unit = models.CharField(null=True, max_length=10)
    chap = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.cat


class MCustomer(Audit):
    custid = models.UUIDField(
        null=False, primary_key=True, default=uuid.uuid4, editable=False)
    custcode = models.BigIntegerField(null=False)
    custname = models.CharField(null=True, max_length=90)
    bname = models.CharField(null=True, max_length=400)
    state = models.CharField(null=True, max_length=30)
    road = models.CharField(null=True, max_length=30)
    city = models.CharField(null=True, max_length=50)
    gstno = models.CharField(null=True, max_length=30)
    payterms = models.CharField(null=True, max_length=50)
    dispatchto = models.CharField(null=True, max_length=50)
    district = models.CharField(null=True, max_length=50)
    invoicetype = models.CharField(null=True, max_length=50)
    panno = models.CharField(null=True, max_length=15)
    statecode = models.CharField(null=True, max_length=10)
    gstinno = models.CharField(null=True, max_length=20)
    agentid = models.ForeignKey(MAgent, on_delete=models.SET_NULL, null=True)
    custtransport = models.CharField(null=True, max_length=60)

    def __str__(self):
        return self.custname


# class MEmployee(Audit):
#     EMPID = models.UUIDField(null=True, default=uuid.uuid5, editable=False)
#     EmpName = models.CharField(null=True, max_length=51)
#     Designation = models.CharField(null=True, max_length=51)
#
#     def __str__(self):
#         return self.EmpName


class MExportFields(Audit):
    exportid = models.UUIDField(null=True, default=uuid.uuid4, editable=False)
    descriptiongoods = models.CharField(null=True, max_length=50)
    hsno = models.CharField(null=True, max_length=50)
    declaration = models.CharField(null=True, max_length=100)
    compcode = models.CharField(null=True, max_length=10)
    declarationline1 = models.CharField(null=True, max_length=100)
    declarationline2 = models.CharField(null=True, max_length=100)
    declarationline3 = models.CharField(null=True, max_length=100)
    declarationline4 = models.CharField(null=True, max_length=100)
    invbackpageheading = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.exportid


class MShade(Audit):
    shadeid = models.UUIDField(
        null=False, primary_key=True, default=uuid.uuid4, editable=False)
    shadecode = models.CharField(null=True, max_length=10)
    shade = models.CharField(null=True, max_length=50)
    apicode = models.CharField(null=True, max_length=10)
    gsm_m = models.FloatField(null=True)
    flaggroup = models.BigIntegerField(null=True)
    batchgroup = models.CharField(null=True, max_length=20)
    fieldgroup = models.CharField(null=True, max_length=10)
    groupcategory = models.BigIntegerField(null=True)
    stocktrans_y_n = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.shadecode


class MItem(Audit):
    itemid = models.UUIDField(null=False, primary_key=True,
                              default=uuid.uuid4, editable=False)
    itemcode = models.CharField(null=True, max_length=20)
    shadeid = models.ForeignKey(MShade, on_delete=models.SET_NULL, null=True)
    sized = models.CharField(null=True, max_length=10)
    gsm = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.itemcode


class MItemCategory(Audit):
    catid = models.UUIDField(null=False, primary_key=True,
                             default=uuid.uuid4, editable=False)
    cat = models.CharField(null=False, max_length=100)
    hsncode = models.CharField(null=True, max_length=20)
    unitid = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True)
    remarks = models.CharField(null=True, max_length=250)

    def __str__(self):
        return self.hsncode


class MLocation(Audit):
    locationid = models.UUIDField(
        null=True, default=uuid.uuid4, editable=False)
    location = models.CharField(null=True, max_length=20)

    def __str__(self):
        return self.location


class MPlusMinusHead(Audit):
    headid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, null=False, editable=False)
    head = models.CharField(null=True, max_length=50)
    plus_minus = models.CharField(null=True, max_length=10)
    api = models.CharField(null=True, max_length=10)
    ref = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.head


class MSupplier(Audit):
    suppid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, null=False, editable=False)
    suppname = models.CharField(null=True, max_length=100)
    bname = models.CharField(null=True, max_length=250)
    area = models.CharField(null=True, max_length=30)
    road = models.CharField(null=True, max_length=30)
    city = models.CharField(null=True, max_length=30)
    pin = models.CharField(null=True, max_length=50)
    state = models.CharField(null=True, max_length=50)
    cell = models.CharField(null=True, max_length=50)
    supptype = models.CharField(null=True, max_length=10)
    gstno = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.suppname


class TInvoice(Audit):
    invoiceid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    custid = models.ForeignKey(
        MCustomer, on_delete=models.SET_NULL, null=True)
    agentid = models.ForeignKey(
        MAgent, on_delete=models.SET_NULL, null=True)
    invoiceno = models.BigIntegerField(null=False)
    invoicedate = models.DateField(null=True,)
    shadeid = models.ForeignKey(
        MShade, on_delete=models.SET_NULL, null=True)
    salestype = models.CharField(null=True, max_length=20)
    pretime = models.TimeField(null=True, max_length=20)
    predate = models.DateField(null=True)
    remtime = models.TimeField(null=True, max_length=20)
    remdate = models.DateField(null=True)
    orderno = models.CharField(null=True, max_length=50)
    orderdate = models.CharField(null=True, max_length=10)
    transport = models.CharField(null=True, max_length=90)
    vehicleno = models.CharField(null=True, max_length=50)
    lrno = models.CharField(null=True, max_length=50)
    lrdate = models.CharField(null=True, max_length=20)
    payterms = models.CharField(null=True, max_length=10)
    remarks = models.CharField(null=True, max_length=60)
    assvalue = models.FloatField(null=True)
    excise = models.CharField(null=True, max_length=10)
    exciseamt = models.FloatField(null=True)
    cess = models.CharField(null=True, max_length=10)
    cessamt = models.FloatField(null=True)
    cst = models.CharField(null=True, max_length=10)
    cstamt = models.FloatField(null=True)
    vat = models.CharField(null=True, max_length=10)
    vatamt = models.FloatField(null=True)
    addvat = models.CharField(null=True, max_length=10)
    addvatamt = models.FloatField(null=True)
    insurance = models.CharField(null=True, max_length=10)
    insuranceamt = models.FloatField(null=True)
    gtotal = models.FloatField(null=True)
    excisesubtotal = models.FloatField(null=True)
    vatsubtotal = models.FloatField(null=True)
    deliveryat = models.CharField(null=True, max_length=60)
    flgtype = models.IntegerField(null=True)
    flgsaletype = models.IntegerField(null=True)
    invoicetype = models.CharField(null=True, max_length=20)
    ind_weight = models.FloatField(null=True)

    def __str__(self):
        return self.invoiceno


class TExport(Audit):
    exportid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    invoiceid = models.ForeignKey(
        TInvoice, on_delete=models.SET_NULL, null=True)
    precarriageby = models.CharField(null=True, max_length=100)
    receiptby = models.CharField(null=True, max_length=100)
    vesselflightno = models.CharField(null=True, max_length=50)
    portofloading = models.CharField(null=True, max_length=90)
    containerno = models.CharField(null=True, max_length=50)
    portofdischarge = models.CharField(null=True, max_length=90)
    paymenttype = models.CharField(null=True, max_length=50)
    empname = models.CharField(null=True, max_length=50)
    empmono = models.CharField(null=True, max_length=50)
    dollarrate = models.FloatField(null=True)
    exchangerate = models.FloatField(null=True)
    dollartotal = models.FloatField(null=True)
    exchagetotal = models.FloatField(null=True)
    noofreels = models.FloatField(null=True)
    containersize = models.CharField(null=True, max_length=50)
    emptyconweight = models.CharField(null=True, max_length=50)
    maxconweight = models.CharField(null=True, max_length=50)
    rfidsealno = models.CharField(null=True, max_length=50)
    linersealno = models.CharField(null=True, max_length=50)
    bankname = models.CharField(null=True, max_length=50)
    paymentterms = models.CharField(null=True, max_length=50)
    shippingbillno = models.CharField(null=True, max_length=50)
    shippingbilldate = models.CharField(null=True, max_length=50)
    weighbridge = models.CharField(null=True, max_length=100)
    hscode = models.CharField(null=True, max_length=50)
    descriptiongoods = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.exportid


class TExportDetails(Audit):
    exportdetailsid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    exportid = models.ForeignKey(TExport, on_delete=models.SET_NULL, null=True)
    reelno = models.FloatField(null=True)
    gweight = models.FloatField(null=True)
    tareweight = models.FloatField(null=True)
    netweight = models.FloatField(null=True)
    invoiceid = models.ForeignKey(
        TInvoice, on_delete=models.SET_NULL, null=True)
    # rewinderid = not there for unit 1
    size = models.CharField(null=True, max_length=20)
    gsm = models.FloatField(null=True)
    noofream_sheets = models.FloatField(null=True)
    uom = models.CharField(null=True, max_length=10)
    dollarrate = models.FloatField(null=True)
    invoiceno = models.CharField(null=True, max_length=10)
    invoicedate = models.DateField(null=True)
    noofream = models.FloatField(null=True)
    reamwt = models.FloatField(null=True)

    def __str__(self):
        return self.exportdetailsid


class TIndent(Audit):
    indentid = models.AutoField(primary_key=True, editable=False)
    custid = models.ForeignKey(MCustomer, on_delete=models.SET_NULL, null=True)
    indentno = models.CharField(null=True, max_length=20)
    indentdate = models.DateField(null=True)
    pono = models.CharField(null=True, max_length=20)
    podate = models.DateField(null=True)
    remark = models.CharField(null=True, max_length=150)

    def __str__(self):
        return self.indentno


class TProduction(Audit):
    productionid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    rdate = models.DateField(null=True)
    l_e = models.CharField(null=True, max_length=10)
    catid = models.ForeignKey(MCategory, on_delete=models.SET_NULL, null=True)
    shadeid = models.ForeignKey(MShade, on_delete=models.SET_NULL, null=True)
    reel_sheet = models.CharField(null=True, max_length=50)
    itemid = models.ForeignKey(MItem, on_delete=models.SET_NULL, null=True)
    length = models.CharField(null=True, max_length=10)
    unitid = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    reelnofrom = models.BigIntegerField(null=False)
    reelnoto = models.BigIntegerField(null=True)
    noofsheet = models.BigIntegerField(null=True)
    noofbdls = models.FloatField(null=True)
    noofream = models.FloatField(null=True)
    reamwt = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    rate = models.FloatField(null=True)
    locationid = models.ForeignKey(
        MLocation, on_delete=models.SET_NULL, null=True)
    indentno = models.CharField(null=True, max_length=20)
    custid = models.ForeignKey(MCustomer, on_delete=models.SET_NULL, null=True)
    agentid = models.ForeignKey(MAgent, on_delete=models.SET_NULL, null=True)
    obflag = models.BooleanField(null=True)  # flag
    apiflag = models.BooleanField(null=True)  # flag
    fac = models.BooleanField(null=True)  # flag
    stk = models.BooleanField(null=True)  # flag
    approved = models.BooleanField(null=True)
    entrytype = models.CharField(null=True, max_length=20)
    stockplus_minus = models.CharField(null=True, max_length=10)
    headid = models.BigIntegerField(null=True, editable=False)
    # for remaining stock removal from inventory
    refproductionid = models.UUIDField(null=True, editable=False)
    lotno = models.CharField(null=True, max_length=60)
    ind_weight = models.FloatField(null=True)
    cm_inch = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.productionid


class TProduction_bck(Audit):
    productionid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    rdate = models.DateField(null=True)
    l_e = models.CharField(null=True, max_length=10)
    catid = models.ForeignKey(MCategory, on_delete=models.SET_NULL, null=True)
    shadeid = models.ForeignKey(MShade, on_delete=models.SET_NULL, null=True)
    reel_sheet = models.CharField(null=True, max_length=50)
    itemid = models.ForeignKey(MItem, on_delete=models.SET_NULL, null=True)
    length = models.CharField(null=True, max_length=10)
    unitid = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    reelnofrom = models.BigIntegerField(null=False)
    reelnoto = models.BigIntegerField(null=True)
    noofsheet = models.BigIntegerField(null=True)
    noofbdls = models.FloatField(null=True)
    noofream = models.FloatField(null=True)
    reamwt = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    rate = models.FloatField(null=True)
    locationid = models.ForeignKey(
        MLocation, on_delete=models.SET_NULL, null=True)
    indentno = models.CharField(null=True, max_length=20)
    custid = models.ForeignKey(MCustomer, on_delete=models.SET_NULL, null=True)
    agentid = models.ForeignKey(MAgent, on_delete=models.SET_NULL, null=True)
    obflag = models.BooleanField(null=True)  # flag
    apiflag = models.BooleanField(null=True)  # flag
    fac = models.BooleanField(null=True)  # flag
    stk = models.BooleanField(null=True)  # flag
    approved = models.BooleanField(null=True)
    entrytype = models.CharField(null=True, max_length=20)
    stockplus_minus = models.CharField(null=True, max_length=10)
    headid = models.BigIntegerField(null=True, editable=False)
    refproductionid = models.UUIDField(null=True, editable=False)
    p_m_remarks = models.CharField(null=True, max_length=60)

    ind_weight = models.FloatField(null=True)
    cm_inch = models.CharField(null=True, max_length=10)


class TProductionReel(Audit):
    productionreelid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    productionid = models.ForeignKey(
        TProduction, on_delete=models.SET_NULL, null=True)
    reelno = models.BigIntegerField(null=True)
    stk = models.CharField(null=True, max_length=10)
    stkdate = models.DateField(null=True)
    invdate = models.DateField(null=True)
    refproductionreelid = models.UUIDField(null=True, editable=False)
