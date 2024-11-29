from django.test import TestCase
from django.utils import safestring
from ..formmod.Displayform import displayDefaultForms as df
# Create your tests here.

class TestdisplayForm(TestCase):

    def setUp(self):
        pass
    def test_loginform(self): 
        self.assertEqual(df.loginForm(),safestring.SafeString())
    def test_Addfield(self):
        pass
        
    
