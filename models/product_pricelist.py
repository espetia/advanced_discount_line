from odoo import models, fields


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    is_generic = fields.Boolean(string='Is Generic', default=False,
                                help='If checked, this pricelist will be available for all customers who do not have a specific permitted pricelist.')
