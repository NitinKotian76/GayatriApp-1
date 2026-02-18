from django.core.exceptions import ValidationError
from django.test import TestCase

from invoice.models import (
    Company,
    TableName,
    TableMetaData,
    TableData,
    CustomUser,
    MAgent,
    MCategory,
    MCustomer,
    MExportFields,
    MShade,
    MItem,
    MItemCategory,
    MItemRate,
    MLocation,
    MPlusMinusHead,
    TInvoice,
    TExport,
    TExportDetails,
    TIndent,
    TProduction,
    TProduction_bck,
    TProductionReel,
)


class TestCoreModels(TestCase):
    def setUp(self) -> None:
        self.company = Company.objects.create(company_name="Test Co")
        self.table = TableName.objects.create(
            table_name="test_table",
            description="Test table",
            company=self.company,
        )

    def test_tabledata_unique_enforced_when_flag_true(self) -> None:
        """TableData.save should prevent duplicates when metadata.table_unique is True."""
        TableMetaData.objects.create(
            table_metadata={"schema": "v1"},
            table_unique=True,
            table_name=self.table,
        )

        data = {"a": 1, "b": 2}
        TableData.objects.create(
            table_data=data,
            table_name=self.table,
            company=self.company,
        )

        with self.assertRaises(ValidationError):
            # Same payload should be rejected for same table/company
            TableData.objects.create(
                table_data={"b": 2, "a": 1},  # different key order, same logical data
                table_name=self.table,
                company=self.company,
            )

    def test_tabledata_allows_duplicates_when_flag_false(self) -> None:
        """When metadata.table_unique is False, duplicates should be allowed."""
        TableMetaData.objects.create(
            table_metadata={"schema": "v1"},
            table_unique=False,
            table_name=self.table,
        )

        data = {"a": 1}
        first = TableData.objects.create(
            table_data=data,
            table_name=self.table,
            company=self.company,
        )
        second = TableData.objects.create(
            table_data=data,
            table_name=self.table,
            company=self.company,
        )

        self.assertNotEqual(first.pk, second.pk)

    def test_custom_user_manager_validation(self) -> None:
        """CustomUser manager should enforce presence of email and emp code."""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="",
                user_name="Foo",
                user_emp_code="123",
                password="dummy",
            )

        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="foo@example.com",
                user_name="Foo",
                user_emp_code="",
                password="dummy",
            )

        user = CustomUser.objects.create_user(
            email="foo@example.com",
            user_name="Foo",
            user_emp_code="E001",
            password="dummy",
            company=self.company,
        )
        self.assertEqual(user.user_emp_code, "E001")
        self.assertTrue(user.check_password("dummy"))


class TestMillsoftMasterModels(TestCase):
    def setUp(self) -> None:
        self.company = Company.objects.create(company_name="Millsoft Co")
        self.agent = MAgent.objects.create(Agentname="Agent A")
        self.category = MCategory.objects.create(Cat="Cat A")
        self.customer = MCustomer.objects.create(
            Custcode=1,
            Custname="Customer A",
            agentid=self.agent,
        )
        self.shade = MShade.objects.create(ShadeCode="SC1")
        self.item = MItem.objects.create(ItemCode="IT1", ShadeID=self.shade)
        self.location = MLocation.objects.create(Location="L1")

    def test_string_representations_do_not_crash(self) -> None:
        """Basic __str__ implementations should return non-empty strings."""
        self.assertTrue(str(self.agent))
        self.assertTrue(str(self.category))
        self.assertTrue(str(self.customer))
        self.assertTrue(str(self.shade))
        self.assertTrue(str(self.item))
        self.assertTrue(str(self.location))

    def test_item_category_and_rate_basic_relations(self) -> None:
        item_category = MItemCategory.objects.create(
            Cat="Item Cat",
            UnitID=self.company,
        )
        rate = MItemRate.objects.create(
            CatID=self.category,
            ItemID=self.item,
            CustID=self.customer,
            AgentID=self.agent,
            Rate=10.0,
        )

        self.assertEqual(rate.CatID, self.category)
        self.assertEqual(rate.ItemID, self.item)
        self.assertEqual(rate.CustID, self.customer)
        self.assertEqual(rate.AgentID, self.agent)
        self.assertTrue(str(item_category))

    def test_plus_minus_head_creation(self) -> None:
        head = MPlusMinusHead.objects.create(head="Head A")
        self.assertEqual(str(head), "Head A")


class TestMillsoftTransactionModels(TestCase):
    def setUp(self) -> None:
        self.company = Company.objects.create(company_name="Tx Co")
        self.agent = MAgent.objects.create(Agentname="Agent B")
        self.category = MCategory.objects.create(Cat="Cat B")
        self.customer = MCustomer.objects.create(
            Custcode=2,
            Custname="Customer B",
            agentid=self.agent,
        )
        self.shade = MShade.objects.create(ShadeCode="SC2")
        self.item = MItem.objects.create(ItemCode="IT2", ShadeID=self.shade)

    def _create_invoice(self) -> TInvoice:
        return TInvoice.objects.create(
            CustID=self.customer,
            AgentID=self.agent,
            InvoiceNo=1,
        )

    def test_invoice_and_export_relations(self) -> None:
        invoice = self._create_invoice()
        export = TExport.objects.create(InvoiceID=invoice)
        detail = TExportDetails.objects.create(
            ExportID=export,
            InvoiceID=invoice,
        )

        self.assertEqual(detail.InvoiceID, invoice)
        self.assertEqual(detail.ExportID, export)

    def test_indent_and_production_relations(self) -> None:
        indent = TIndent.objects.create(
            CustID=self.customer,
            IndentNo="IND1",
        )

        production = TProduction.objects.create(
            CatID=self.category,
            ShadeID=self.shade,
            ItemID=self.item,
            UnitID=self.company,
            ReelNoFrom=1,
            LocationID=MLocation.objects.create(Location="L2"),
            CustID=self.customer,
            AgentID=self.agent,
        )

        production_bck = TProduction_bck.objects.create(
            CatID=self.category,
            ShadeID=self.shade,
            ItemID=self.item,
            UnitID=self.company,
            ReelNoFrom=1,
            LocationID=production.LocationID,
            CustID=self.customer,
            AgentID=self.agent,
        )

        reel = TProductionReel.objects.create(ProductionID=production)

        self.assertEqual(str(indent), "IND1")
        self.assertEqual(reel.ProductionID, production)
        self.assertEqual(production.CustID, self.customer)
        self.assertEqual(production_bck.CatID, self.category)

