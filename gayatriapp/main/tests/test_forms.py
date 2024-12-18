from django.test import TestCase, Client
from django.utils import safestring
from ..formmod import DefaultForm as df
# Create your tests here.

class TestdisplayForm(TestCase):

    def setUp(self):
        pass

    def test_loginform(self): 
        response= self.client.get("main:login")
        self.assertEqual(response.status_code, 200)

    def test_Addfield(self):
        pass
        
