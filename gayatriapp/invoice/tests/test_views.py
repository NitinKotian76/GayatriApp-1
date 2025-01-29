from django.test import TestCase, Client
from django.urls import reverse

class TestViews(TestCase):
    def setup(self):
        client = Client(enforce_csrf_checks=False)

    def test_create_form_view(self):
        response = self.client.get("/main/create_form")
        self.assertEqual(response.status_code, 200)

    def test_form_setup_view(self):
        response = self.client.get("/main/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("home.html")
        response = self.client.post("/main/form_setup",
                                        {   "Username":"nixon",
                                            "Password":"nixon",
                                            "select*Company":"company1",
                                            "Login":"Login"
                                        }
                                    )
        self.assertTemplateUsed("index.html")
        self.assertRedirects(response,"/main/edit_form")

    def test_form_config_page(self):
        response = self.client.get("/main/create_form")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("index.html")

    # def test_delete_config(self):
    #     response = self.client.post("/main/delete_form")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.context, "success")

