from django import forms
import logging
from ..models import *
from django.utils.html import *
from ..dbmod import dbfunctions as db

logger = logging.getLogger(__name__)

# Custom Forms#

# admin forms


class adminCompany(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

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

class customer(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    order_types = [("local", "Local"),
                   ("direct", "Direct"),
                   ("export", "Export"),
                   ]

    customer_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w3-input'}), max_length=50)
    agent_or_customer_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w3-input'}), max_length=50)
    address_details = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w3-input'}), max_length=1000)
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w3-input'}), max_length=50)
    state = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w3-input'}), max_length=50)
    pin_code = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'w3-input'}), max_value=999999)
    gst_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w3-input'}), min_length=15, max_length=15)
    pan_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w3-input'}), min_length=10, max_length=10)
    payment_term = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'w3-input'}))  # payment period in days
    dispatch_to = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w3-input'}), max_length=50)
    district = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w3-input'}), max_length=50)
    invoice_type = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'w3-input'}), choices=order_types)


class supplier(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    order_types = [("local", "Local"),
                   ("direct", "Direct"),
                   ("export", "Export"),
                   ]
    supplier_name = forms.CharField(max_length=50)
    agent_or_supplier_name = forms.CharField(max_length=50)
    address_details = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    pin_code = forms.IntegerField()
    gst_no = forms.IntegerField()
    pan_no = forms.CharField(max_length=50)
    payment_term = forms.IntegerField()  # payment period in days
    dispatch_to = forms.CharField(max_length=50)
    district = forms.CharField(max_length=50)
    invoice_type = forms.ChoiceField(choices=order_types)


class signatory(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    signatory_name = forms.CharField(max_length=50)
    designation = forms.CharField(max_length=50)


class export_fields(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    description_of_goods = forms.CharField(max_length=50)
    hsn_code = forms.CharField(max_length=50)
    tax_declaration = forms.CharField(max_length=50)
    invoice_back_page_heading = forms.CharField(max_length=50)


class item_category(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    category = forms.CharField(max_length=50)
    unit = forms.CharField(max_length=50)
    hsn_code = forms.CharField(max_length=50)
    remarks = forms.CharField(max_length=50)


class variety(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
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
    stock_transfer = forms.ChoiceField(choices=[(True, "yes"), (False, "no")])


class items(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    item_code = forms.CharField(max_length=50)
    variety = forms.CharField(max_length=50)
    deckle_size = forms.DecimalField()
    gsm = forms.DecimalField()


class stock(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    category = forms.CharField(max_length=50)
    plus_minus = forms.CharField(max_length=50)
    api = forms.ChoiceField(choices=[(True, "yes"), (False, "no")])
    reference = forms.ChoiceField(choices=[(True, "with"), (False, "without")])


class units(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    unit_of_measurement = forms.CharField()


class location(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    location = forms.CharField()


# transaction#


class open_bal_prod(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    template_name = "form_snippet.html"
    order_types = [("local", "Local"),
                   ("export", "Export"),
                   ]

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    plus_minus_head = forms.ChoiceField(
        choices=[(True, "plus"), (False, "minus")])
    local_or_export = forms.ChoiceField(choices=order_types)
    variety = forms.ChoiceField(choices=[])
    type = forms.ChoiceField(choices=[])
    item_code = forms.ChoiceField(choices=[])
    size = forms.DecimalField()
    length = forms.DecimalField()
    gsm = forms.IntegerField()
    unit = forms.ChoiceField(choices=[])
    no_of_bdls = forms.IntegerField()  # no of bundles
    excise_no_from = forms.IntegerField()
    excise_no_to = forms.IntegerField()
    no_of_sheets = forms.IntegerField()
    ream_weight = forms.DecimalField()
    no_of_ream = forms.IntegerField()
    weight = forms.DecimalField()
    rate = forms.DecimalField()
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
                "variety", "variety", user_id)
            self.fields['type'].choices = db.get_choices(
                "items", "item_type", user_id)
            self.fields['item_code'].choices = db.get_choices(
                "items", "item_code", user_id)
            self.fields['unit'].choices = db.get_choices(
                "units", "unit_of_measurement", user_id)
            self.fields['location'].choices = db.get_choices(
                "location", "location", user_id)
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", user_id)
            self.fields['agent'].choices = db.get_choices(
                "agent", "agent_name", user_id)


class production(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    template_name = "form_snippet.html"

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
    size = forms.DecimalField()
    length = forms.DecimalField()
    gsm = forms.IntegerField()
    unit = forms.ChoiceField(choices=[])
    no_of_bdls = forms.IntegerField()  # no of bundles
    excise_no_from = forms.IntegerField()
    excise_no_to = forms.IntegerField()
    no_of_sheets = forms.IntegerField()
    ream_weight = forms.DecimalField()
    no_of_ream = forms.IntegerField()
    weight = forms.DecimalField()
    rate = forms.DecimalField()
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
                "variety", "variety", user_id)
            self.fields['item_type'].choices = db.get_choices(
                "items", "item_type", user_id)
            self.fields['item_code'].choices = db.get_choices(
                "items", "item_code", user_id)


class prod_plus_minus(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    template_name = "form_snippet.html"
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
    size = forms.DecimalField()
    length = forms.DecimalField()
    gsm = forms.IntegerField()
    unit = forms.ChoiceField(choices=[])
    no_of_bdls = forms.IntegerField()  # no of bundles
    excise_no_from = forms.IntegerField()
    excise_no_to = forms.IntegerField()
    no_of_sheets = forms.IntegerField()
    ream_weight = forms.DecimalField()
    no_of_ream = forms.IntegerField()
    weight = forms.DecimalField()
    rate = forms.DecimalField()
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
                "variety", "variety", user_id)
            self.fields['item_type'].choices = db.get_choices(
                "items", "item_type", user_id)
            self.fields['item_code'].choices = db.get_choices(
                "items", "item_code", user_id)
            self.fields['unit'].choices = db.get_choices(
                "units", "unit_of_measurement", user_id)
            self.fields['location'].choices = db.get_choices(
                "location", "location", user_id)
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", user_id)
            self.fields['agent'].choices = db.get_choices(
                "agent", "agent_name", user_id)


class prod_approval(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    # tableview


class invoice(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
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

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['variety'].choices = db.get_choices(
                "variety", "variety", user_id)
            self.fields['transport'].choices = db.get_choices(
                "transport", "transport", user_id)
            self.fields['supervisor_name'].choices = db.get_choices(
                "supervisor", "supervisor_name", user_id)
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


class jumbo_roll_qc(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    shift = forms.ChoiceField()
    jumbo_roll_no = forms.IntegerField()
    variety = forms.ChoiceField(choices=[])
    # formset
    # # (in_gsm)
    gsm = forms.DecimalField()
    # # (in_microns)
    caliper = forms.DecimalField()
    # # (cc/gm)
    bulk = forms.DecimalField()
    # (in g/m2)
    cobb_top = forms.DecimalField()
    # (in g/m2)
    cobb_bottom = forms.DecimalField()
    # (in %)
    moisture_avg = forms.DecimalField()
    # (md/cd)(gm-cm)
    taber_stiffness = forms.DecimalField()
    ratio = forms.DecimalField()
    brightness = forms.DecimalField()
    gloss = forms.DecimalField()
    # (in_sec)
    soat = forms.DecimalField()
    # (microns)
    pps_roughness = forms.DecimalField()
    # (mts/sec)
    igt_dry_pick = forms.DecimalField()
    # (scott) (ft.lb in thousands)
    ply_bond = forms.DecimalField()
    surface_ph = forms.DecimalField()
    surface_dust = forms.DecimalField()
    top_formation = forms.DecimalField()
    varnishability = forms.DecimalField()
    cracking_creasing = forms.DecimalField()
    flatness = forms.DecimalField()

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['variety'].choices = db.get_choices(
                "variety", "variety", user_id)


class lot_no_wise_qc(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    order_types = [("local", "Local"),
                   ("export", "Export"),
                   ]
    lot_no = forms.IntegerField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    jumbo_roll_no = forms.IntegerField()
    variety = forms.ChoiceField(choices=[])
    gsm = forms.DecimalField()
    local_or_export = forms.ChoiceField(choices=order_types)
    type_reel_or_sheet = forms.ChoiceField()
    size = forms.DecimalField()
    item_code = forms.ChoiceField(choices=[])
    unit = forms.ChoiceField(choices=[])
    location = forms.ChoiceField(choices=[])
    indent_no = forms.IntegerField()
    party = forms.ChoiceField(choices=[])
    agent = forms.ChoiceField(choices=[])
    weight = forms.DecimalField()

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['variety'].choices = db.get_choices(
                "variety", "variety", user_id)
            self.fields['item_code'].choices = db.get_choices(
                "items", "item_code", user_id)
            self.fields['unit'].choices = db.get_choices(
                "units", "unit_of_measurement", user_id)
            self.fields['location'].choices = db.get_choices(
                "location", "location", user_id)
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", user_id)
            self.fields['agent'].choices = db.get_choices(
                "agent", "agent_name", user_id)


class finishing_house(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    order_types = [("local", "Local"),
                   ("export", "Export"),
                   ]

    lot_no = forms.IntegerField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    jumbo_roll_no = forms.IntegerField()
    variety = forms.ChoiceField(choices=[])
    gsm = forms.DecimalField()
    local_or_export = forms.ChoiceField(choices=order_types)
    type_reel_or_sheet = forms.ChoiceField()
    size = forms.DecimalField()
    item_code = forms.ChoiceField(choices=[])
    unit = forms.ChoiceField(choices=[])
    location = forms.ChoiceField(choices=[])
    indent_no = forms.IntegerField()
    party = forms.ChoiceField(choices=[])
    agent = forms.ChoiceField(choices=[])
    weight = forms.DecimalField()

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['variety'].choices = db.get_choices(
                "variety", "variety", user_id)
            self.fields['item_code'].choices = db.get_choices(
                "items", "item_code", user_id)
            self.fields['unit'].choices = db.get_choices(
                "units", "unit_of_measurement", user_id)
            self.fields['location'].choices = db.get_choices(
                "location", "location", user_id)
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", user_id)
            self.fields['agent'].choices = db.get_choices(
                "agent", "agent_name", user_id)


class program_planing(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    # all customer planning/ per customer planning
    planning = forms.ChoiceField(choices=[])
    Sr_No = forms.IntegerField()
    gsm = forms.DecimalField()
    size_deckle = forms.DecimalField()
    cutting = forms.DecimalField()
    qty = forms.IntegerField()
    ream_wt = forms.DecimalField()
    customer_name = forms.ChoiceField(choices=[])
    indent_no = forms.IntegerField()

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['planning'].choices = db.get_choices(
                "planning", "planning", user_id)
            self.fields['customer_name'].choices = db.get_choices(
                "customer", "customer_name", user_id)

# report #


class pending_order(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", user_id)
            # logger.debug(self.fields['party'].choices)


class prod_record(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", user_id)


class dispatch_details(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", user_id)


class stock_report(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"


class loader_report(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", user_id)


class qc_report(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", user_id)


class stock_plus_minus(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    party = forms.ChoiceField(choices=[])
    export_to = forms.FileField()

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['party'].choices = db.get_choices(
                "customer", "customer_name", user_id)
