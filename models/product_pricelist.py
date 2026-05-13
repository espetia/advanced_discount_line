from odoo import models, fields


class ProductPricelist(models.Model):
    """
    Inherits from product.pricelist to allow marking certain pricelists as generic.
    """
    _inherit = 'product.pricelist'

    # If enabled, this pricelist is considered 'generic' and available to any customer
    # who doesn't have a specific set of permitted pricelists.
    is_generic = fields.Boolean(string='Is Generic', default=False,
                                help='If checked, this pricelist will be available for all customers who do not have a specific permitted pricelist.')
