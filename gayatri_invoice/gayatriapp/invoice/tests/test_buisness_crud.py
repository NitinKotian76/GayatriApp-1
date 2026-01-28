from django.test import TestCase
from ..dbmod import dbfunctions as db


class buiseness_crud(TestCase):
    def setUp(self):
        db.set_data()

    def test_set_data_in_production_table(self):
        pass

    def test_update
