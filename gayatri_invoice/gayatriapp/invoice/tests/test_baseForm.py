from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.utils import safestring
from ..formmod import Base as BF


class TestBaseForm(TestCase):
    def setup():
        setup_test_environment()
        client = Client(enforce_csrf_checks=False)

    def test_method_list(self):
        # check if the methods return a string
        methodlist = BF.appControls.getInputFields()

        for method_name in methodlist:
            method = getattr(BF.base, method_name, None)
            if callable(method):
                out = method("<i>demo</i>", label="label",
                             attr="demo", valid="true")
                typecheck = type(out)
                if type(out) == safestring.SafeString:
                    print(f"{method_name} is okay {typecheck}")
                else:
                    print(f"{method_name} not okay {typecheck}")
            else:
                print(method_name+"\tnot callable")

    def test_request_header_data_foreach_field(self):
        # this might need selenium
        methodlist = BF.appControls.getInputFields()
        excludeList = ["modalContainer", "container", "fieldset",
                       "columnContainer", "form", "list", "search", "file"]
        formfields = ""

        for method_name in methodlist:
            method = getattr(BF.base, method_name, None)
            if method_name not in excludeList:
                continue
                if callable(method):
                    out = method(children="<i>demo</i>",
                                 label="label", attr="required", valid="true")
                    formfields += out
        # this basically test all the general fields with one form and does a post request and we check if the data recieved is correct
        reponse = self.client.post("main:form_setup")
        BF.base.form(children=formfields)
