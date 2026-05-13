from odoo import models, api, fields

class Partner(models.Model):
    _inherit = 'res.partner'

    permitted_price_list_ids = fields.Many2many('product.pricelist', string='Permitted Price Lists', help='List of price lists that the user is allowed to use.')

