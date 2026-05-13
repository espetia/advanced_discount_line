from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """
    Inherits from sale.order to restrict price lists based on partner permissions.
    """
    _inherit = 'sale.order'

    # Technical field to store the price lists allowed for the selected partner
    partner_permitted_price_list_ids = fields.Many2many('product.pricelist', string='Permitted Price List', invisible=1,
                                                        store=False)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Updates the permitted price lists when the partner changes.
        If the partner has specific price lists, use them; otherwise, use generic price lists.
        """
        res = super(SaleOrder, self).onchange_partner_id()
        for order in self:
            order.pricelist_id = False
            if order.partner_id:
                if order.partner_id.permitted_price_list_ids:
                    order.partner_permitted_price_list_ids = order.partner_id.permitted_price_list_ids
                else:
                    generic_pricelists = self.env['product.pricelist'].search([('is_generic', '=', True)])
                    order.partner_permitted_price_list_ids = generic_pricelists

        return res

    @api.constrains('pricelist_id', 'partner_id')
    def _check_pricelist_id_permitted(self):
        """
        Validates that the selected price list is allowed for the partner.
        Raises a ValidationError if the price list is not permitted.
        """
        for order in self:
            if order.partner_id and order.pricelist_id:
                permitted_pricelists = order.partner_id.permitted_price_list_ids
                if not permitted_pricelists:
                    permitted_pricelists = self.env['product.pricelist'].search([('is_generic', '=', True)])

                if permitted_pricelists and order.pricelist_id not in permitted_pricelists:
                    raise ValidationError(_(
                        'The price list "%s" is not permitted for customer %s. '
                        'Please select one of the authorized lists (including generic ones if applicable).'
                    ) % (order.pricelist_id.name, order.partner_id.name))


