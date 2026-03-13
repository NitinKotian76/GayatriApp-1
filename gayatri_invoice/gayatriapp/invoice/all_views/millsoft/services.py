from ...models import (MItem, TProduction, TProductionReel, MCustomer)
from django.db.models import Max
import logging
logger = logging.getLogger(__name__)

def _get_reel_numbers(excise_from, excise_to):
    """Return list of reel numbers from excise_from to excise_to (inclusive)."""
    try:
        start = int(excise_from) if excise_from else 0
        end = int(excise_to) if excise_to else start
        if start <= end:
            count = end - start + 1
            return list(range(start, end + 1))
    except (ValueError, TypeError):
        pass
    return []

def _autocomplete_form_data(data):
    """Build form data with preserved user values and computed size, gsm, weight, excise fields."""
    form_data = data.copy()
    if hasattr(form_data, '_mutable'):
        form_data._mutable = True

    itemcode_val = data.get("itemcode", "")
    noofbdls = data.get("noofbdls", "")
    noofream = data.get("noofream", "")
    reamwt = data.get("reamwt", "")
    size = data.get("size", "")
    gsm = data.get("gsm", "")
    noofsheet = data.get("noofsheet", "")
    length = data.get("length", "")
    type_of_reel_sheet = data.get("type_of_reel_sheet", "")
    formula = data.get("formula", "")
    # Get MItem by pk (ForeignKey value) or by itemcode string
    itemcode_obj = None
    if itemcode_val:
        try:
            itemcode_obj = MItem.objects.get(pk=itemcode_val)
        except (MItem.DoesNotExist, ValueError):
            itemcode_obj = MItem.objects.filter(itemcode=itemcode_val).first()

    if itemcode_obj:
        form_data["size"] = itemcode_obj.size or ""
        form_data["gsm"] = itemcode_obj.gsm or ""
    
    form_data["formula"] = formula

    # only for bundle and pallet, we need to calculate the reamwt based on the size, length, gsm and noofsheet
    if type_of_reel_sheet.startswith("BUNDLE") or type_of_reel_sheet.startswith("PALLET")  or type_of_reel_sheet.startswith("BULK") and formula=="true":
        if size and gsm and noofsheet and length:
            try:
                form_data["reamwt"] = str(round(float(size) * float(length) * float(gsm)* float(noofsheet)/10000000,1)) # in kg
            except (ValueError, TypeError):
                logger.error(f"Error calculating reamwt: {size}, {gsm}, {noofsheet}, {length}")
        # these are constants
        reamwt_float = form_data.get("reamwt", "")
        r= float(reamwt_float) if str(reamwt_float).strip() else 0
        noofream = 0
        b = float(noofbdls) if str(noofbdls).strip() else 0

        # calculate the noofream based on the reamwt thresholds
        if r >= 10.0 and r < 12.6:
            noofream=6.0
        elif r >= 12.6 and r <=13.5:
            noofream=5.0
        elif r >= 13.6 and r <= 17.5:
            noofream=4.0
        elif r>=17.6 and r <= 24.5:
            noofream=3.0
        elif r>=24.6 and r <= 32.5:
            noofream=2.0
        elif r>=32.6 :
            noofream=1.0
        else:
            # minimum reamwt is 10.0
            noofream=0.0

        if r and noofream:
            form_data["weight"] = str(round(r * noofream * b,1))

        form_data["noofream"] = str(noofream)

        last_reel = TProductionReel.objects.aggregate(Max('reelno'))['reelno__max'] 
        base_reelno = int(last_reel) + 1 if last_reel else 1
        form_data["excise_from"] = str(base_reelno)
        if noofbdls:
            try:
                form_data["excise_to"] = str(base_reelno + int(float(noofbdls)))
            except (ValueError, TypeError):
                form_data["excise_to"] = str(base_reelno)
        
    return form_data

def _set_invoice_productions_out_of_stock(invoice):
    """Set stk=False on all TProduction records linked to this invoice via TInvoiceDetails."""
    productions = TProduction.objects.filter(custid_id=invoice.custid_id, agentid_id=invoice.agentid_id, shadeid_id=invoice.shadeid_id, stk=True)
    if productions:
        productions.update(stk=False)


def _set_selected_reels_and_productions_out_of_stock(invoice, selected_reel_ids):
    """
    Set stk=False on the given TProductionReel records (by pk) and their parent TProduction records.
    Link those productions to the invoice and clear reels' stk flag (CharField -> "").
    """
    if not selected_reel_ids:
        return
    reels = TProductionReel.objects.filter(pk__in=selected_reel_ids).select_related("productionid")
    if not reels.exists():
        return
    production_ids = list(reels.values_list("productionid_id", flat=True).distinct())
    TProduction.objects.filter(pk__in=production_ids).update(stk=False)
    TProductionReel.objects.filter(pk__in=selected_reel_ids).update(stk=False)
    invoice.productionid.add(*production_ids)

def _get_productionreel_list_data(data,qs):
    custid = data.get("custid", "")
    agentid = data.get("agentid", "")
    shadeid = data.get("shadeid", "")
    logger.info(f"custid: {custid}, agentid: {agentid}, shadeid: {shadeid}")
    if custid and agentid and shadeid:
        productionids= TProduction.objects.filter(
            custid=custid, agentid=agentid, shadecode=shadeid,
             stk=True).values("pk")
        qs= qs.filter(pk__in=productionids) # productionreel qs
        logger.info(f"productionids: {productionids}")
    else:
        productionids = TProduction.objects.filter(
            stk=True).values("pk")
        qs= qs.filter(pk__in=productionids) # productionreel qs 
        logger.info(f"productionids: {productionids}")
    return qs

def _agentid_from_custid(initial):
    """Set the agentid based on the custid."""
    if initial.get("custid"):
        custid = initial.get("custid")
        initial["agentid"] = MCustomer.objects.get(custid=custid).agentid
    return initial

# def _shadeid_from_itemcode(initial):
#     """Set the shadeid based on the itemcode."""
#     if initial.get("itemcode"):
#         itemcode = initial.get("itemcode")
#         logger.info(f"itemcode: {itemcode}")
#         initial["shadeid"] = MItem.objects.get(itemid=itemcode).shadeid
#     return initial

def _itemcode_from_shadeid(initial):
    """Set the itemcode based on the shadeid."""
    if initial.get("shadeid") and initial.get("gsm") and initial.get("size"):
        shadeid = initial.get("shadeid")
        gsm = initial.get("gsm")
        size = initial.get("size")
        itemcode = f"{shadeid}{size}{gsm}" # shadeid is alphanumeric, size is 4 digits, gsm is 3 digits
        initial["itemcode"] = itemcode
    return initial


def _set_initial_values_from_form_data(initial, form_data):
    """Set the initial values from the form data."""
    for key, value in form_data.items():
        initial[key] = value
    return initial

def _data_for_reel_preview(form_data):
    """Get the data for the reel preview."""
    weight = form_data.get("weight", "")
    # noofbdls = form_data.get("noofbdls", "") # no of bdls per pallet or bundle is always 1
    noofream = form_data.get("noofream", "")
    reamwt = form_data.get("reamwt", "")
    reamwt_int = 0
    noofream_int = 0
    try:
        reamwt_int = round(float(reamwt),1) if reamwt else 0
        noofream_int = round(float(noofream),1) if noofream else 0
        weight_per_row = round(reamwt_int * noofream_int,1)
        noofbdls_per_row = 1
        noofream_per_row = noofream_int
    except (ValueError, TypeError):
        reamwt_int = 0
        noofream_int = 0
        weight_per_row = 0
        noofbdls_per_row = 1
        noofream_per_row = 0
    reel_numbers = _get_reel_numbers(
        form_data.get("excise_from"),
        form_data.get("excise_to"),
    )
    excise_from = form_data.get("excise_from") or 0
    excise_to = form_data.get("excise_to") or excise_from
    try:
        reel_total = int(excise_to) - int(excise_from) if excise_from and excise_to else len(reel_numbers)
    except (ValueError, TypeError):
        reel_total = len(reel_numbers)
    
    context = {
                "reel_numbers": reel_numbers,
                "reel_total": reel_total,
                "weight": weight,
                "noofbdls_per_row": noofbdls_per_row,
                "noofream_per_row": noofream_per_row,
                "reamwt_per_row": reamwt_int,
                "weight_per_row": weight_per_row,
            }
    return context



CHUNK_SIZE = 8192

def _stream_file(file_path, chunk_size=CHUNK_SIZE):
    with open(file_path, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data