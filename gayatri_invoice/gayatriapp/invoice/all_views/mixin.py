class TableViewMixin:
    list_url_name = None
    trigger_event = 'tableUpdate'

 # context['modelurl'] = self.request.path.rsplit('/', 2)[0]  get the self url
    # def get_success_response(self, success_message=
