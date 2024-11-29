from django.test import TestCase
from django.utils import safestring
from ..formmod import BaseForm as BF

class TestBaseForm(TestCase):

    def test_method_list(self):
        # check if the methods return a string
        appc= BF.appControls()
        methodlist = appc.getInputFields()

        for method_name in methodlist:
            method = getattr(BF.base,method_name,None)
            if callable(method):
                out = method("<i>demo</i>",label="label",attr="demo")
                typecheck=type(out)
                if type(out) == safestring.SafeString:
                    print(f"{method_name} is okay {typecheck}")
                else:
                    print(f"{method_name} not okay {typecheck}")
            else:
                print(method_name+"\tnot callable")

