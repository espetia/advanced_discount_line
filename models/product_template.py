from odoo import models, fields

class ProductTemplate(models.Model):
    """
    Inherits from product.template to add configuration for price unit editing.
    """
    _inherit = 'product.template'

    # Determines if the unit price of this product can always be edited in Sale Orders
    always_edit_price_unit = fields.Boolean(
        string="Always Edit Unit Price",
        help="If checked, the unit price can be edited in sale orders regardless of user permissions.",
        default=False
    )
