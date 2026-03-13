from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
import os

from .services import _stream_file


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