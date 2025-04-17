# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestDeliveryPackageNumberDefault(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Test product", "type": "product"}
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.picking_type_id = cls.env.ref("stock.picking_type_internal")
        cls.picking_type_id.write({"default_number_of_packages": 10})
        cls.wh1 = cls.env["stock.warehouse"].create(
            {"name": "TEST WH1", "code": "TST1"}
        )

    def test_default_number(self):
        picking = (
            self.env["stock.picking"]
            .with_context(restricted_picking_type_code=self.picking_type_id.code)
            .create(
                {
                    "location_id": self.wh1.lot_stock_id.id,
                    "location_dest_id": self.wh1.wh_output_stock_loc_id.id,
                    "picking_type_id": self.picking_type_id.id,
                }
            )
        )
        self.assertEqual(picking.number_of_packages, 10)
