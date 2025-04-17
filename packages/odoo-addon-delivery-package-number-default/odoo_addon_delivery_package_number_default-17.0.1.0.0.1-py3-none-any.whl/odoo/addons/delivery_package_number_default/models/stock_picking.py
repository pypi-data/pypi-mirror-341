# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _default_number_of_packages(self, picking_type_id=False):
        picking_type_code = self.env.context.get("restricted_picking_type_code")
        picking_type = False
        if picking_type_code:
            picking_type_code = self.env.context.get("restricted_picking_type_code")
            picking_type = self.env["stock.picking.type"].search(
                [
                    ("code", "=", picking_type_code),
                    ("company_id", "=", self.env.company.id),
                ],
                limit=1,
            )
        elif picking_type_id:
            picking_type = (
                self.env["stock.picking.type"].browse(picking_type_id).exists()
            )
        return picking_type and picking_type.default_number_of_packages or 1

    number_of_packages = fields.Integer(
        default=lambda self: self._default_number_of_packages(),
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not (
                self.env.context.get("restricted_picking_type_code")
                or vals.get("number_of_packages")
            ):
                vals["number_of_packages"] = self._default_number_of_packages(
                    vals.get("picking_type_id")
                )
        res = super().create(vals)
        return res
