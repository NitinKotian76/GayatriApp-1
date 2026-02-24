from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, HttpResponse, StreamingHttpResponse
from django.template.loader import render_to_string
from django.urls import (reverse_lazy, reverse)
from django.views import View
from django_htmx.http import trigger_client_event
from django.db.models.functions import Cast
from django.db.models import CharField
from xlsxtpl.writerx import BookWriter

from ...form_files import (helperFunct as hf, millsoftForm as mf)

from weasyprint import HTML
from io import BytesIO
import os
import uuid
import csv
import logging

logger = logging.getLogger(__name__)

CHUNK_SIZE = 8192


def _stream_file(file_path, chunk_size=CHUNK_SIZE):
    with open(file_path, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data


class RChallanCreateView(View):
    """Create a challan PDF and redirect to its download URL."""

    def post(self, request, *args, **kwargs):
        logger.debug("the pdf view ran")
        pdf_buffer = BytesIO()
        template = request.POST.get("template")
        context = request.POST.get("context")
        template_path = os.path.join(settings.MEDIA_ROOT, "ReportTemplates", "DemoTemplate.html")
        html_string = render_to_string(
            "DemoTemplate.html", context
        )
        logger.debug(html_string)
        HTML(string=html_string).write_pdf(pdf_buffer)

        filename = f"challan_{uuid.uuid4().hex[:8]}.pdf"
        pdf_path = os.path.join(settings.MEDIA_ROOT, "Challans", filename)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        with open(pdf_path, "wb") as f:
            f.write(pdf_buffer.getvalue())

        download_url = reverse("invoice:download_challan", args=[filename])

        messages.success(request, "pdf created")
        response = HttpResponse("pdf created")
        response["HX-Redirect"] = download_url
        return response

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=204)


class DownloadPdfView(View):
    """Stream a challan PDF for download."""

    def get(self, request, filename, *args, **kwargs):
        pdf_path = os.path.join(settings.MEDIA_ROOT, "Challans", filename)

        if not os.path.exists(pdf_path):
            return HttpResponse("file not found", status=404)

        response = StreamingHttpResponse(
            _stream_file(pdf_path),
            content_type="application/pdf",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class DownloadCsvView(View):
    """Stream a report CSV for download."""

    def get(self, request, filename, *args, **kwargs):
        csv_path = os.path.join(settings.MEDIA_ROOT, "Reports", filename)

        if not os.path.exists(csv_path):
            return HttpResponse("file not found", status=404)

        response = StreamingHttpResponse(
            _stream_file(csv_path),
            content_type="text/csv",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

class DownloadExcelView(View):
    """Stream a report Excel for download."""

    def get(self, request, filename, *args, **kwargs):
        excel_path = os.path.join(settings.MEDIA_ROOT, "Reports", filename)

        if not os.path.exists(excel_path):
            return HttpResponse("file not found", status=404)

        response = StreamingHttpResponse(
            _stream_file(excel_path),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

class RInvoiceCreateView(View):
    """Create a invoice PDF and redirect to its download URL."""

    def post(self, request, *args, **kwargs):
        return HttpResponse(status=204)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=204)

class RDispatchDetailsCreateView(View):
    """Create a dispatch details PDF and redirect to its download URL."""

    def post(self, request, *args, **kwargs):
        return HttpResponse(status=204)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=204)

class RGatePassCreateView(View):
    """Create a gate pass PDF and redirect to its download URL."""

    def post(self, request, *args, **kwargs):
        return HttpResponse(status=204)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=204)


class RStockCreateView(View):
    """Create a stock PDF and redirect to its download URL."""

    def post(self, request, *args, **kwargs):
        return HttpResponse(status=204)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=204)