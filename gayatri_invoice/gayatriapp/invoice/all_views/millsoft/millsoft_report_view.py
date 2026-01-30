from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, HttpResponse, StreamingHttpResponse
from django.template.loader import render_to_string
from django.urls import (reverse_lazy, reverse)
from django_htmx.http import trigger_client_event
from django.db.models.functions import Cast
from django.db.models import CharField

from ...form_files import (helperFunct as hf, millsoftForm as mf)

from weasyprint import HTML
from io import BytesIO
import os
import uuid
import csv
import logging
logger = logging.getLogger(__name__)


def RChallan_create(request):
    if request.method == "POST":
        logger.debug("the pdf view ran")
        pdf_buffer = BytesIO()

        html_string = render_to_string(
            "DemoTemplate.html", {"company_name": "GAYATRISHAKTI PAPER AND BOARDS LTD"})
        logger.debug(html_string)
        # weasy
        HTML(string=html_string).write_pdf(pdf_buffer)

        filename = f"challan_{uuid.uuid4().hex[:8]}.pdf"
        pdf_path = os.path.join(settings.MEDIA_ROOT, "Challans", filename)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        with open(pdf_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())

        download_url = reverse("invoice:download_challan", args=[filename])

        messages.success(request, "pdf created")
        response = HttpResponse("pdf created")
        response["HX-Redirect"] = download_url
        return response
    return HttpResponse(status=204)


def download_challan(request, filename):
    pdf_path = os.path.join(settings.media_root, "Challans", filename)

    if not os.path.exists(pdf_path):
        return httpresponse("file not found", status=404)

    def file_iterator(file_path, chunk_size=8192):
        with open(pdf_path, "rb") as f:
            while true:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data

    response = streaminghttpresponse(
        file_iterator(pdf_path),
        content_type="application/pdf")
    response['content-disposition'] = f'attachment;filename="{filename}"'
    return response

def download_csv(request, filename):
    csv_path = os.path.join(settings.media_root, "Reports", filename)

    if not os.path.exists(csv_path):
        return httpresponse("file not found", status=404)

    def file_iterator(file_path, chunk_size=8192):
        with open(csv_path, "rb") as f:
            while true:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data

    response = streaminghttpresponse(
        file_iterator(csv_path),
        content_type="text/csv")
    response['content-disposition'] = f'attachment;filename="{filename}"'
    return response

class RPendingOrder():
    pass
