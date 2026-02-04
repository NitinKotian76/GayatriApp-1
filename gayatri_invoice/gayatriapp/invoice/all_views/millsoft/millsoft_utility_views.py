import logging
logger = logging.getLogger(__name__)


def StockTransfer(request):
    """
    for transferring stock from one agent/customer/excessStocklot to another 
    """
    if request.method == "POST":
