from . import BaseForm as bf
from . import formComponents
from django import forms
from django.core.exceptions import ValidationError
import logging
import json
from ..models import *
from django.utils.html import *

logger = logging.getLogger(__name__)

# Custom Forms#

# TODO: all master forms need a search field
# masters #


def tableview(model):
    # TODO: this just checks if the table is callable
    # but need a way to access the table
    table = model
    MODEL_HEADERS = [f.name for f in table._meta.fields]
    query_results = [list(i.values())
                     for i in list(table.objects.all().values())]
    # return a response to your template and add query_results to the context
    header, column, row = "", "", ""
    for item in MODEL_HEADERS:
        header += f'<th>{item}</th>'

    for all_rows in query_results:
        for every_column in all_rows:
            column += f'<td>{every_column}</td>'

        row = f'<tr>{column}</tr>'

    table_html = format_html(
        f'<table class="w3-table-all"><tr>{header}</tr>{row}</table>')
    return table_html


def button(name):
    data = json.dumps({"form": name})
    buttons = format_html('<input class="w3-button w3-padding w3-margin"\
                type="submit" value="submit" \
                hx-post="/invoice/form_view"\
                hx-target="#mainform" \
                hx-swap="innerHTML" \
                hx-vals=\'{}\'/>', data)
    return buttons


class customer(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    customer_name = forms.SlugField()
    agent_or_customer_name = forms.SlugField()
    address_details = forms.CharField(max_length=1000)
    city = forms.SlugField()
    state = forms.SlugField()
    pin_code = forms.IntegerField(max_value=999999)
    gst_no = forms.CharField(min_length=15, max_length=15)
    pan_no = forms.CharField(min_length=10, max_length=10)
    payment_term = forms.IntegerField()  # payment period in days
    dispatch_to = forms.SlugField()
    district = forms.SlugField()
    invoice_type = forms.SlugField()


class supplier(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"

    supplier_name = forms.SlugField()
    agent_or_supplier_name = forms.SlugField()
    address_details = forms.SlugField()
    city = forms.SlugField()
    state = forms.SlugField()
    pin_code = forms.IntegerField()
    gst_no = forms.IntegerField()
    pan_no = forms.SlugField()
    payment_term = forms.IntegerField()  # payment period in days
    dispatch_to = forms.SlugField()
    district = forms.SlugField()
    invoice_type = forms.SlugField()


class signatory(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    signatory_name = forms.SlugField()
    designation = forms.SlugField()


class export_fields(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    description_of_goods = forms.SlugField()
    hsn_code = forms.SlugField()
    tax_declaration = forms.SlugField()
    invoice_back_page_heading = forms.SlugField()


class item_category(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    category = forms.SlugField()
    unit = forms.SlugField()
    hsn_code = forms.SlugField()
    remarks = forms.SlugField()


class variety(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    code = forms.SlugField()
    shade_code = forms.SlugField()
    # api grouping
    api_code = forms.IntegerField()
    api_gsm = forms.IntegerField()
    # challan report
    flag_group = forms.IntegerField()
    batch_group = forms.IntegerField()
    field_group = forms.SlugField()
    # stock report grouping
    group_category = forms.IntegerField()
    stock_transfer = forms.ChoiceField(choices=("yes", "no"))


class items(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    item_code = forms.SlugField()
    variety = forms.SlugField()
    deckle_size = forms.DecimalField()
    gsm = forms.DecimalField()


class stock(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    category = forms.SlugField()
    plus_minus = forms.SlugField()
    api = forms.ChoiceField(choices=("true", "false"))
    reference = forms.ChoiceField(choices=("with", "without"))


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
    date = forms.DateField()
    plus_minus_head = forms.ChoiceField(choices=("plus", "minus"))
    local_or_export = forms.ChoiceField(choices=("local", "export"))
    variety = forms.ChoiceField()
    type = forms.ChoiceField()
    item_code = forms.ChoiceField()
    size = forms.DecimalField()
    length = forms.DecimalField()
    gsm = forms.IntegerField()
    unit = forms.ChoiceField()
    no_of_bdls = forms.ChoiceField()  # no of bundles
    excise_no_from = forms.IntegerField()
    excise_no_to = forms.IntegerField()
    no_of_sheets = forms.IntegerField()
    ream_weight = forms.DecimalField()
    no_of_ream = forms.IntegerField()
    weight = forms.DecimalField()
    rate = forms.DecimalField()
    location = forms.ChoiceField()
    indent_no = forms.IntegerField()
    party = forms.ChoiceField()
    agent = forms.ChoiceField()
    fsc = forms.ChoiceField(choices=("yes", "no"))
    lot_no = forms.IntegerField()
    # tableview()


class prod_record(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    template_name = "form_snippet.html"
    date = forms.DateField()
    plus_minus_head = forms.ChoiceField(choices=("plus", "minus"))
    local_or_export = forms.ChoiceField(choices=("local", "export"))
    variety = forms.ChoiceField()
    type = forms.ChoiceField()
    item_code = forms.ChoiceField()
    size = forms.DecimalField()
    length = forms.DecimalField()
    gsm = forms.IntegerField()
    unit = forms.ChoiceField()
    no_of_bdls = forms.ChoiceField()  # no of bundles
    excise_no_from = forms.IntegerField()
    excise_no_to = forms.IntegerField()
    no_of_sheets = forms.IntegerField()
    ream_weight = forms.DecimalField()
    no_of_ream = forms.IntegerField()
    weight = forms.DecimalField()
    rate = forms.DecimalField()
    location = forms.ChoiceField()
    indent_no = forms.IntegerField()
    party = forms.ChoiceField()
    agent = forms.ChoiceField()
    fsc = forms.ChoiceField(choices=("yes", "no"))
    lot_no = forms.IntegerField()


class prod_plus_minus(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    template_name = "form_snippet.html"
    date = forms.DateField()
    plus_minus_head = forms.ChoiceField(choices=("plus", "minus"))
    local_or_export = forms.ChoiceField(choices=("local", "export"))
    variety = forms.ChoiceField()
    type = forms.ChoiceField()
    item_code = forms.ChoiceField()
    size = forms.DecimalField()
    length = forms.DecimalField()
    gsm = forms.IntegerField()
    unit = forms.ChoiceField()
    no_of_bdls = forms.ChoiceField()  # no of bundles
    excise_no_from = forms.IntegerField()
    excise_no_to = forms.IntegerField()
    no_of_sheets = forms.IntegerField()
    ream_weight = forms.DecimalField()
    no_of_ream = forms.IntegerField()
    weight = forms.DecimalField()
    rate = forms.DecimalField()
    location = forms.ChoiceField()
    indent_no = forms.IntegerField()
    party = forms.ChoiceField()
    agent = forms.ChoiceField()
    fsc = forms.ChoiceField(choices=("yes", "no"))
    lot_no = forms.IntegerField()


class prod_approval(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    date = forms.DateField()
    # tableview


class invoice_direct(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    party = forms.SlugField()
    agent = forms.SlugField()
    chalan_no = forms.IntegerField()
    chalan_date = forms.DateField()
    invoice_no = forms.IntegerField()
    invoice_date = forms.DateField()
    variety = forms.ChoiceField()
    sales_type = forms.ChoiceField()
    pre_time_date = forms.DateTimeField()
    rem_time_date = forms.DateTimeField()
    order_no = forms.IntegerField()
    order_date = forms.DateField()
    transport = forms.ChoiceField()
    vehicle_no = forms.CharField()
    supervisor_name = forms.ChoiceField()
# table_view
    remark = forms.SlugField()
    delivery_at = forms.SlugField()
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
    date = forms.DateField()
    shift = forms.ChoiceField()
    jumbo_roll_no = forms.IntegerField()
    variety = forms.ChoiceField()
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


class lot_no_wise_qc(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    lot_no = forms.IntegerField()
    date = forms.DateField()
    jumbo_roll_no = forms.IntegerField()
    variety = forms.ChoiceField()
    gsm = forms.DecimalField()
    local_or_export = forms.ChoiceField()
    type_reel_or_sheet = forms.ChoiceField()
    size = forms.DecimalField()
    item_code = forms.ChoiceField()
    unit = forms.CharField()
    location = forms.ChoiceField()
    indent_no = forms.CharField()
    party = forms.ChoiceField()
    agent = forms.ChoiceField()
    weight = forms.DecimalField()


class finishing_house(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"


class Programme_planing(forms.Form):
    template_name = "form_snippet.html"
    error_css_class = "error"
    required_css_class = "required"
    # all customer planning/ per customer planning
    planning = forms.ChoiceField()
    Sr_No = forms.IntegerField()
    gsm = forms.DecimalField()
    size_deckle = forms.DecimalField()
    cutting = forms.DecimalField()
    qty = forms.IntegerField()
    ream_wt = forms.DecimalField()
    customer_name = forms.CharField()
    indent_no = forms.IntegerField()
