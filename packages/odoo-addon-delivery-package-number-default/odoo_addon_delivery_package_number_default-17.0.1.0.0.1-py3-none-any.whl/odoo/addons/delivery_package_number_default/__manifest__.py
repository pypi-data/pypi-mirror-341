# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Delivery PAckage Number Default",
    "summary": "Set a default value in delivery package number to not call the wizard",
    "version": "17.0.1.0.0",
    "category": "Stock",
    "website": "https://github.com/sygel-technology/sy-delivery-carrier",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "delivery_package_number",
    ],
    "data": ["views/stock_picking_type_views.xml"],
}
