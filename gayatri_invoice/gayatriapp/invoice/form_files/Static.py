from django import forms
import logging
from ..models import *
from django.utils.html import *
from ..dbmod import dbfunctions as db

logger = logging.getLogger(__name__)

# Custom Forms#

# admin forms


class formClass(forms.Form):
    """
    common class for all forms with same properties

    Attributes:
        template_name (str): html snippet name to use as a template
        error_css_class (str): css class for error
        required_css_class (str): css class for required
    """
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop("user_id", None)
        super().__init__(*args, **kwargs)


class adminCompany(formClass):

    company_name = forms.ModelChoiceField(
        queryset=Company.objects.none(),
        empty_label="Select Company",
        widget=forms.Select(attrs={}),
        to_field_name="id",
        label="company_name",
        required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].queryset = Company.objects.all()


# TODO: all master forms need a search field for faster filtering

# masters #

class customer(formClass):
    order_types = [("local", "Local"),
                   ("direct", "Direct"),
                   ("export", "Export"),
                   ]

    customer_name = forms.CharField(widget=forms.TextInput(), max_length=50)
    agent_or_customer_name = forms.CharField(
        widget=forms.TextInput(), max_length=50)
    address_details = forms.CharField(
        widget=forms.TextInput(), max_length=1000)
    city = forms.CharField(widget=forms.TextInput(), max_length=50)
    state = forms.CharField(widget=forms.TextInput(), max_length=50)
    pin_code = forms.IntegerField(widget=forms.TextInput(), max_value=999999)
    gst_no = forms.CharField(widget=forms.TextInput(),
                             min_length=15, max_length=15)
    pan_no = forms.CharField(widget=forms.TextInput(),
                             min_length=10, max_length=10)
    payment_term = forms.IntegerField(
        widget=forms.TextInput())  # payment period in days
    dispatch_to = forms.CharField(widget=forms.TextInput(), max_length=50)
    district = forms.CharField(widget=forms.TextInput(), max_length=50)
    invoice_type = forms.ChoiceField(
        widget=forms.Select(), choices=order_types)


class supplier(formClass):
    order_types = [("local", "Local"),
                   ("direct", "Direct"),
                   ("export", "Export"),
                   ]
    supplier_name = forms.CharField(max_length=50)
    agent_or_supplier_name = forms.CharField(max_length=50)
    address_details = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    pin_code = forms.IntegerField(widget=forms.TextInput(), max_value=999999)
    gst_no = forms.CharField(widget=forms.TextInput(),
                             min_length=15, max_length=15)
    pan_no = forms.CharField(widget=forms.TextInput(),
                             min_length=10, max_length=10)
    payment_term = forms.IntegerField()  # payment period in days
    dispatch_to = forms.CharField(max_length=50)
    district = forms.CharField(max_length=50)
    invoice_type = forms.ChoiceField(choices=order_types)


class signatory(formClass):

    signatory_name = forms.CharField(max_length=50)
    designation = forms.CharField(max_length=50)


class export_fields(formClass):

    description_of_goods = forms.CharField(max_length=50)
    hsn_code = forms.CharField(max_length=50)
    tax_declaration = forms.CharField(max_length=50)
    invoice_back_page_heading = forms.CharField(max_length=50)


class item_category(formClass):

    category = forms.CharField(max_length=50)
    unit = forms.CharField(max_length=50)
    hsn_code = forms.CharField(max_length=50)
    remarks = forms.CharField(max_length=50)


class variety(formClass):

    code = forms.CharField(max_length=50)
    shade_code = forms.CharField(max_length=50)
    # api grouping
    api_code = forms.IntegerField()
    api_gsm = forms.IntegerField()
    # challan report
    flag_group = forms.IntegerField()
    batch_group = forms.IntegerField()
    field_group = forms.CharField(max_length=50)
    # stock report grouping
    group_category = forms.IntegerField()
    stock_transfer = forms.NullBooleanField(
        widget=forms.Select(choices=[(True, "yes"), (False, "no")]))


class item_name(formClass):

    item_code = forms.CharField(max_length=50)
    variety = forms.CharField(max_length=50)
    deckle_size = forms.FloatField()
    gsm = forms.FloatField()


class stock(formClass):

    category = forms.CharField(max_length=50)
    plus_minus = forms.CharField(max_length=50)
    api = forms.NullBooleanField(widget=forms.Select(
        choices=[(True, "yes"), (False, "no")]))
    reference = forms.NullBooleanField(widget=forms.Select(
        choices=[(True, "with"), (False, "without")]))


class location(formClass):

    location = forms.CharField()


class units(formClass):

    unit = forms.CharField()


class stock_transfer(formClass):

    party = forms.ChoiceField(choices=[])
    agent = forms.ChoiceField(choices=[])
    indent_no = forms.CharField()


# transaction#


class open_bal_prod(formClass):

    order_types = [("local", "Local"),
                   ("export", "Export"),
                   ]

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    plus_minus_head = forms.ChoiceField(
        choices=[(True, "plus"), (False, "minus")])
    local_or_export = forms.ChoiceField(choices=order_types)
    variety = forms.ChoiceField(choices=[])
    item_type = forms.ChoiceField(choices=[])
    item_code = forms.ChoiceField(choices=[])
    size = forms.FloatField()
    length = forms.FloatField()
    gsm = forms.IntegerField()
    unit = forms.ChoiceField(choices=[])
    no_of_bdls = forms.IntegerField()  # no of bundles
    excise_no_from = forms.IntegerField()
    excise_no_to = forms.IntegerField()
    no_of_sheets = forms.IntegerField()
    ream_weight = forms.FloatField()
    no_of_ream = forms.IntegerField()
    weight = forms.FloatField()
    rate = forms.FloatField()
    location = forms.ChoiceField(choices=[])
    indent_no = forms.IntegerField()
    party = forms.ChoiceField(choices=[])
    agent = forms.ChoiceField(choices=[])
    fsc = forms.BooleanField()
    lot_no = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['variety'].choices = db.get_choices(
                "variety", "code", self.user_id)
            self.fields['item_type'].choices = db.get_choices(
                "item_name", "gsm", self.user_id)
            self.fields['item_code'].choices = db.get_choices(
                "item_name", "item_code", self.user_id)
            self.fields['unit'].choices = db.get_choices(
                "units", "unit", self.user_id)
            self.fields['location'].choices = db.get_choices(
                "location", "location", self.user_id)
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", self.user_id)
            self.fields['agent'].choices = db.get_choices(
                "customer", "agent_or_customer_name", self.user_id)


class production(formClass):

    order_types = [("local", "Local"), ("export", "Export")]
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    plus_minus_head = forms.ChoiceField(
        choices=[(True, "plus"), (False, "minus")])
    local_or_export = forms.ChoiceField(choices=order_types)
    variety = forms.ChoiceField(choices=[])
    item_type = forms.ChoiceField(choices=[])
    item_code = forms.ChoiceField(choices=[])
    size = forms.FloatField()
    length = forms.FloatField()
    gsm = forms.IntegerField()
    unit = forms.ChoiceField(choices=[])
    no_of_bdls = forms.IntegerField()  # no of bundles
    excise_no_from = forms.IntegerField()
    excise_no_to = forms.IntegerField()
    no_of_sheets = forms.IntegerField()
    ream_weight = forms.FloatField()
    no_of_ream = forms.IntegerField()
    weight = forms.FloatField()
    rate = forms.FloatField()
    location = forms.ChoiceField(choices=[])
    indent_no = forms.IntegerField()
    party = forms.ChoiceField(choices=[])
    agent = forms.ChoiceField(choices=[])
    fsc = forms.BooleanField()
    lot_no = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id:
            self.fields['variety'].choices = db.get_choices(
                "variety", "code", self.user_id)
            self.fields['item_type'].choices = db.get_choices(
                "item_name", "variety", self.user_id)
            self.fields['item_code'].choices = db.get_choices(
                "item_name", "item_code", self.user_id)
            self.fields['location'].choices = db.get_choices(
                "location", "location", self.user_id)
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", self.user_id)
            self.fields['agent'].choices = db.get_choices(
                "customer", "agent_or_customer_name", self.user_id)
            self.fields['unit'].choices = db.get_choices(
                "units", "unit", self.user_id)


class prod_plus_minus(formClass):

    order_types = [("local", "Local"),
                   ("export", "Export"),
                   ]
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    plus_minus_head = forms.ChoiceField(
        choices=[(True, "plus"), (False, "minus")])
    local_or_export = forms.ChoiceField(choices=order_types)
    variety = forms.ChoiceField(choices=[])
    item_type = forms.ChoiceField(choices=[])
    item_code = forms.ChoiceField(choices=[])
    size = forms.FloatField()
    length = forms.FloatField()
    gsm = forms.IntegerField()
    unit = forms.ChoiceField(choices=[])
    no_of_bdls = forms.IntegerField()  # no of bundles
    excise_no_from = forms.IntegerField()
    excise_no_to = forms.IntegerField()
    no_of_sheets = forms.IntegerField()
    ream_weight = forms.FloatField()
    no_of_ream = forms.IntegerField()
    weight = forms.FloatField()
    rate = forms.FloatField()
    location = forms.ChoiceField(choices=[])
    indent_no = forms.IntegerField()
    party = forms.ChoiceField(choices=[])
    agent = forms.ChoiceField(choices=[])
    fsc = forms.ChoiceField(choices=[(True, "yes"), (False, "no")])
    lot_no = forms.IntegerField()

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['variety'].choices = db.get_choices(
                "variety", "variety", self.user_id)
            self.fields['item_type'].choices = db.get_choices(
                "items", "item_type", self.user_id)
            self.fields['item_code'].choices = db.get_choices(
                "items", "item_code", self.user_id)
            self.fields['unit'].choices = db.get_choices(
                "units", "unit", self.user_id)
            self.fields['location'].choices = db.get_choices(
                "location", "location", self.user_id)
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", self.user_id)
            self.fields['agent'].choices = db.get_choices(
                "agent", "agent_name", self.user_id)


class prod_approval(formClass):

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    # tableview


class invoice(formClass):

    order_types = [("local", "Local"),
                   ("direct", "Direct"),
                   ("export", "Export"),
                   ]
    party = forms.CharField(max_length=50)
    agent = forms.CharField(max_length=50)
    chalan_no = forms.IntegerField()
    chalan_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    invoice_no = forms.IntegerField()
    invoice_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    variety = forms.ChoiceField(choices=[])
    sales_type = forms.ChoiceField(choices=order_types)
    pre_time_date = forms.DateTimeField()
    rem_time_date = forms.DateTimeField()
    order_no = forms.IntegerField()
    order_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    transport = forms.ChoiceField(choices=[])
    vehicle_no = forms.CharField()
    supervisor_name = forms.ChoiceField(choices=[])
    remark = forms.CharField(max_length=50)
    delivery_at = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['variety'].choices = db.get_choices(
                "variety", "variety", self.user_id)
            self.fields['transport'].choices = db.get_choices(
                "transport", "transport", self.user_id)
            self.fields['supervisor_name'].choices = db.get_choices(
                "supervisor", "supervisor_name", self.user_id)
# table_view
# Exciseno, Quality, Variety, Size, Length, GSM, NO of bundles, No of stream, Stream wt., Weight, Unit, Rate, Amount
# output table view
# ass_value
# insurance
# cgst
# sgst
# igst
# grand_total
# buttons
# add
# edit
# delete
# QCtest
# GAtePass
# challan
# invoice
# Find


class jumbo_roll_qc(formClass):

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    shift = forms.ChoiceField()
    jumbo_roll_no = forms.IntegerField()
    variety = forms.ChoiceField(choices=[])
    # formset
    # # (in_gsm)
    gsm = forms.FloatField()
    # # (in_microns)
    caliper = forms.FloatField()
    # # (cc/gm)
    bulk = forms.FloatField()
    # (in g/m2)
    cobb_top = forms.FloatField()
    # (in g/m2)
    cobb_bottom = forms.FloatField()
    # (in %)
    moisture_avg = forms.FloatField()
    # (md/cd)(gm-cm)
    taber_stiffness = forms.FloatField()
    ratio = forms.FloatField()
    brightness = forms.FloatField()
    gloss = forms.FloatField()
    # (in_sec)
    soat = forms.FloatField()
    # (microns)
    pps_roughness = forms.FloatField()
    # (mts/sec)
    igt_dry_pick = forms.FloatField()
    # (scott) (ft.lb in thousands)
    ply_bond = forms.FloatField()
    surface_ph = forms.FloatField()
    surface_dust = forms.FloatField()
    top_formation = forms.FloatField()
    varnishability = forms.FloatField()
    cracking_creasing = forms.FloatField()
    flatness = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['variety'].choices = db.get_choices(
                "variety", "variety", self.user_id)


class lot_no_wise_qc(formClass):

    order_types = [("local", "Local"),
                   ("export", "Export"),
                   ]
    lot_no = forms.IntegerField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    jumbo_roll_no = forms.IntegerField()
    variety = forms.ChoiceField(choices=[])
    gsm = forms.FloatField()
    local_or_export = forms.ChoiceField(choices=order_types)
    type_reel_or_sheet = forms.ChoiceField()
    size = forms.FloatField()
    item_code = forms.ChoiceField(choices=[])
    unit = forms.ChoiceField(choices=[])
    location = forms.ChoiceField(choices=[])
    indent_no = forms.IntegerField()
    party = forms.ChoiceField(choices=[])
    agent = forms.ChoiceField(choices=[])
    weight = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['variety'].choices = db.get_choices(
                "variety", "variety", self.user_id)
            self.fields['item_code'].choices = db.get_choices(
                "items", "item_code", self.user_id)
            self.fields['unit'].choices = db.get_choices(
                "units", "unit", self.user_id)
            self.fields['location'].choices = db.get_choices(
                "location", "location", self.user_id)
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", self.user_id)
            self.fields['agent'].choices = db.get_choices(
                "agent", "agent_name", self.user_id)


class finishing_house(formClass):

    order_types = [("local", "Local"),
                   ("export", "Export"),
                   ]

    lot_no = forms.IntegerField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    jumbo_roll_no = forms.IntegerField()
    variety = forms.ChoiceField(choices=[])
    gsm = forms.FloatField()
    local_or_export = forms.ChoiceField(choices=order_types)
    type_reel_or_sheet = forms.ChoiceField()
    size = forms.FloatField()
    item_code = forms.ChoiceField(choices=[])
    unit = forms.ChoiceField(choices=[])
    location = forms.ChoiceField(choices=[])
    indent_no = forms.IntegerField()
    party = forms.ChoiceField(choices=[])
    agent = forms.ChoiceField(choices=[])
    weight = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['variety'].choices = db.get_choices(
                "variety", "variety", self.user_id)
            self.fields['item_code'].choices = db.get_choices(
                "items", "item_code", self.user_id)
            self.fields['unit'].choices = db.get_choices(
                "units", "unit", self.user_id)
            self.fields['location'].choices = db.get_choices(
                "location", "location", self.user_id)
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", self.user_id)
            self.fields['agent'].choices = db.get_choices(
                "agent", "agent_name", self.user_id)


class program_planing(formClass):

    # all customer planning/ per customer planning
    planning = forms.ChoiceField(choices=[])
    Sr_No = forms.IntegerField()
    gsm = forms.FloatField()
    size_deckle = forms.FloatField()
    cutting = forms.FloatField()
    qty = forms.IntegerField()
    ream_wt = forms.FloatField()
    customer_name = forms.ChoiceField(choices=[])
    indent_no = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['planning'].choices = db.get_choices(
                "planning", "planning", self.user_id)
            self.fields['customer_name'].choices = db.get_choices(
                "customer", "customer_name", self.user_id)

# report #


class pending_order(formClass):

    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['party'].choices = [(None, "--------")] + db.get_choices(
                "customer", "customer_name", self.user_id)
            # logger.debug(self.fields['party'].choices)


class prod_record(formClass):

    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['party'].choices = [(None, "--------")] + db.get_choices(
                "customer", "customer_name", self.user_id)


class dispatch_details(formClass):

    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['party'].choices = [(None, "--------")] + db.get_choices(
                "customer", "customer_name", self.user_id)


class stock_report(formClass):

    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['party'].choices = [(None, "--------")] + db.get_choices(
                "customer", "customer_name", self.user_id)


class loader_report(formClass):

    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['party'].choices = [(None, "--------")] + db.get_choices(
                "customer", "customer_name", self.user_id)


class qc_report(formClass):

    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['party'].choices = [(None, "--------")] + db.get_choices(
                "customer", "customer_name", self.user_id)


class stock_plus_minus(formClass):

    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_id is not None:
            self.fields['party'].choices = [(None, "--------")] + db.get_choices(
                "customer", "customer_name", self.user_id)
