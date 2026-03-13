from django.views import View
from django.shortcuts import render
from .services import _data_for_reel_preview
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import HttpResponse

@method_decorator(never_cache, name='dispatch')
class ReelPreview(View):
    """
    For previewing the reel numbers and their details.
    Sends no-cache headers so the browser/proxy never reuse a stale response.
    """
    def get(self, request, *args, **kwargs):
        form_data = request.GET
        if not form_data:
            return HttpResponse("No form data provided", status=400)
        reel_preview_context = _data_for_reel_preview(form_data)
        response = render(request, "partials/reel_preview.html", reel_preview_context)
        # Explicit no-cache so reel preview never shows stale data
        response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response