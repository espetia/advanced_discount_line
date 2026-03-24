from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    always_edit_price_unit = fields.Boolean(
        string="Always Edit Unit Price",
        help="If checked, the unit price can be edited in sale orders regardless of user permissions.",
        default=False
    )
