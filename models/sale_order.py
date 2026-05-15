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

    state = fields.Selection(
        selection_add=[
            ('draft',),
            ('pending_approval', 'Pending Approval'),
            ('approved', 'Approved'),
            ('sent',),
            ('sale',),
            ('done',),
            ('cancel',),
        ],
        ondelete={'pending_approval': 'set default', 'approved': 'set default'}
    )
    current_approver_id = fields.Many2one('res.users', string='Current Approver', copy=False, tracking=True)
    current_approval_step_id = fields.Many2one('discount.approval.chain', string='Current Approval Step', copy=False)
    is_current_approver = fields.Boolean(compute='_compute_is_current_approver')
    requires_approval = fields.Boolean(compute='_compute_requires_approval')

    @api.depends('order_line.discount', 'order_line.product_id')
    def _compute_requires_approval(self):
        for order in self:
            requires = False
            for line in order.order_line:
                if not line.discount:
                    continue
                configs = self.env['discount.line.configuration'].search([('discount', '=', line.discount)])
                if not configs:
                    continue
                user_permitted = False
                for config in configs:
                    if order.env.user.id in config.permited_users.ids:
                        user_permitted = True
                        break
                if not user_permitted:
                    requires = True
                    break
            order.requires_approval = requires

    @api.depends('current_approver_id')
    def _compute_is_current_approver(self):
        for order in self:
            order.is_current_approver = order.current_approver_id == self.env.user

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        res = super(SaleOrder, self).message_post(**kwargs)
        if self.env.context.get('mark_so_as_sent'):
            self.filtered(lambda o: o.state == 'approved').with_context(tracking_disable=True).write({'state': 'sent'})
        return res

    def action_request_approval(self):
        for order in self:
            max_discount = max([line.discount or 0.0 for line in order.order_line] or [0.0])
            requires_approval = False
            
            for line in order.order_line:
                if not line.discount:
                    continue
                configs = self.env['discount.line.configuration'].search([('discount', '=', line.discount)])
                if not configs:
                    continue
                
                # Check if current user is permitted in ANY valid config
                user_permitted = False
                for config in configs:
                    if order.env.user.id in config.permited_users.ids:
                        user_permitted = True
                        break
                
                if not user_permitted:
                    requires_approval = True
                    break
            
            if requires_approval:
                chains = self.env['discount.approval.chain'].search([
                    ('min_percent', '<=', max_discount)
                ], order='min_percent asc')
                
                if chains:
                    first_chain = chains[0]
                    order.write({
                        'state': 'pending_approval',
                        'current_approver_id': first_chain.approver_id.id,
                        'current_approval_step_id': first_chain.id
                    })
                    
                    template = self.env.ref('advanced_discount_line.email_template_discount_approval', raise_if_not_found=False)
                    if template:
                        kanban_url = "/web#id=%s&model=sale.order&view_type=form" % order.id
                        template.with_context(kanban_url=kanban_url).send_mail(order.id, force_send=True)
                else:
                    # No config for this max % -> auto approve
                    order.write({'state': 'approved'})
            else:
                order.write({'state': 'approved'})

    def action_confirm(self):
        for order in self:
            requires_approval = False
            
            for line in order.order_line:
                if not line.discount:
                    continue
                configs = self.env['discount.line.configuration'].search([('discount', '=', line.discount)])
                if not configs:
                    continue
                
                # Check if current user is permitted in ANY valid config
                user_permitted = False
                for config in configs:
                    if order.env.user.id in config.permited_users.ids:
                        user_permitted = True
                        break
                
                if not user_permitted:
                    requires_approval = True
                    break
            
            if requires_approval and order.state not in ['approved', 'sent']:
                raise ValidationError(_("This order requires discount approval before it can be confirmed. Please request approval first."))

        return super(SaleOrder, self).action_confirm()

    def action_approve_discount(self):
        for order in self:
            if order.state == 'pending_approval' and order.current_approver_id == self.env.user:
                max_discount = max([line.discount or 0.0 for line in order.order_line] or [0.0])
                chains = self.env['discount.approval.chain'].search([
                    ('min_percent', '<=', max_discount)
                ], order='min_percent asc')
                
                next_chain = False
                found_current = False
                for chain in chains:
                    if found_current:
                        next_chain = chain
                        break
                    if chain.id == order.current_approval_step_id.id:
                        found_current = True
                
                if next_chain:
                    order.write({
                        'current_approver_id': next_chain.approver_id.id,
                        'current_approval_step_id': next_chain.id
                    })
                    template = self.env.ref('advanced_discount_line.email_template_discount_approval', raise_if_not_found=False)
                    if template:
                        kanban_url = "/web#id=%s&model=sale.order&view_type=form" % order.id
                        template.with_context(kanban_url=kanban_url).send_mail(order.id, force_send=True)
                else:
                    order.write({
                        'state': 'approved',
                        'current_approver_id': False,
                        'current_approval_step_id': False
                    })
                    approved_template = self.env.ref('advanced_discount_line.email_template_discount_approved', raise_if_not_found=False)
                    if approved_template:
                        kanban_url = "/web#id=%s&model=sale.order&view_type=form" % order.id
                        approved_template.with_context(kanban_url=kanban_url).send_mail(order.id, force_send=True)

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


