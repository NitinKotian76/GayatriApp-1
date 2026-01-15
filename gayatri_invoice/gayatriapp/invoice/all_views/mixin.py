class TableViewMixin:
    list_url_name = None
    trigger_event = 'tableUpdate'

    def get_success_response(self, success_message=None):
        response = HttpResponse(status=204)
