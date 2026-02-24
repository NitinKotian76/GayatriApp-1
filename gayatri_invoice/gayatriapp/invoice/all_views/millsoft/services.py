def _set_invoice_productions_out_of_stock(invoice):
    """Set stk=False on all TProduction records linked to this invoice via TInvoiceDetails."""
    production_ids = (
        TInvoiceDetails.objects.filter(invoiceid=invoice)
        .exclude(productionid_id__isnull=True)
        .values_list("productionid_id", flat=True)
    )
    if production_ids:
        TProduction.objects.filter(pk__in=production_ids).update(stk=False)

def _set_invoice_details(invoice):
    pass