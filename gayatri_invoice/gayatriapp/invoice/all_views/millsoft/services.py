from ...models import (MItem, TProduction, TProductionReel)

def _get_reel_numbers(excise_from, excise_to, max_preview=50):
    """Return list of reel numbers from excise_from to excise_to (inclusive). Capped for preview."""
    try:
        start = int(excise_from) if excise_from else 0
        end = int(excise_to) if excise_to else start
        if start <= end:
            count = end - start + 1
            if count <= max_preview:
                return list(range(start, end + 1))
            return list(range(start, start + max_preview))  # Show first N
    except (ValueError, TypeError):
        pass
    return []

def _get_dynamic_form_data(data):
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
    
    # reamwt (ind_weight) is only calculated when type is not REEL
    if type_of_reel_sheet != "REEL" and size and gsm and noofsheet and length:
        try:
            sheet_area = float(size) * float(length)/10000 # if in cm then convert to m
            form_data["reamwt"] = str(int(sheet_area * float(gsm))* int(noofsheet)/1000) # in kg
        except (ValueError, TypeError):
            pass

    if reamwt and noofream:
        try:
            r = float(reamwt) if str(reamwt).strip() else 0
            n = float(noofream) if str(noofream).strip() else 0
            b = float(noofbdls) if str(noofbdls).strip() else 0
            if r and n:
                form_data["weight"] = str(int(r * n * b))
        except (ValueError, TypeError):
            pass

    last_reel = TProductionReel.objects.last()
    base_reelno = int(last_reel.reelno) + 1 if last_reel else 1
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

def _get_productionreel_list_data(data,qs):
    custid = data.get("custid", "")
    agentid = data.get("agentid", "")
    shadeid = data.get("shadeid", "")
    if custid and agentid and shadeid:
        productionids= TProduction.objects.filter(
            custid_id=custid, agentid_id=agentid, shadecode_id=shadeid,
             stk=True).values_list("productionid", flat=True)
        if productionids:   
            qs= qs.filter(productionid_id__in=productionids)
        else:
            return qs.none()
    else:
        productionids = TProduction.objects.filter(
            stk=True).values_list("productionid", flat=True)
        if productionids:
            qs= qs.filter(productionid_id__in=productionids)
        else:
            return qs.none()
    return qs

