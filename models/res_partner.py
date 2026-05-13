from odoo import models, api, fields

class Partner(models.Model):
    """
    Inherits from res.partner to define which price lists are permitted for a customer.
    """
    _inherit = 'res.partner'

    # List of price lists that this specific partner is allowed to use in Sale Orders
    permitted_price_list_ids = fields.Many2many('product.pricelist', string='Permitted Price Lists', help='List of price lists that the user is allowed to use.')

