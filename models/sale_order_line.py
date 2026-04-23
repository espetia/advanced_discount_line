from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_price_unit_editable = fields.Boolean(
        compute='_compute_is_price_unit_editable'
    )
    increment = fields.Float(string="Increment (%)", digits='Discount', default=0.0)

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        if self.increment:
            res['price_unit'] = res.get('price_unit', self.price_unit) * (1 + (self.increment or 0.0) / 100.0)
        return res

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'increment')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0) * (1 + (line.increment or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    @api.depends('product_id', 'product_id.always_edit_price_unit')
    def _compute_is_price_unit_editable(self):
        has_group = self.env.user.has_group('advanced_discount_line.permit_edit_price_unit')
        for line in self:
            product_override = line.product_id and line.product_id.always_edit_price_unit
            line.is_price_unit_editable = has_group or product_override

    @api.constrains('discount', 'product_id', 'product_uom_qty', 'price_unit')
    def _check_advanced_discount(self):
        for line in self:
            discount = line.discount
            if not discount or line.display_type:  # Ignore notes or sections (if any)
                continue

            configs = self.env['discount.line.configuration'].search([('discount', '=', discount)])
            if not configs:
                raise ValidationError(
                    _("The %s%% discount is not part of the rules permitted by the business.") % discount
                )

            today = fields.Date.context_today(line)
            current_user = self.env.user
            
            product_template_id = line.product_id.product_tmpl_id.id if line.product_id else False
            qty = line.product_uom_qty
            price = line.price_unit
            amount = qty * price

            is_valid = False
            all_errors = []

            for config in configs:
                config_errors = []

                if config.permited_products and product_template_id not in config.permited_products.ids:
                    config_errors.append(_("- The product is not among those allowed by the rule."))

                if config.valid_from and today < config.valid_from:
                    config_errors.append(_("- Rule valid only from %s.") % config.valid_from)
                if config.valid_to and today > config.valid_to:
                    config_errors.append(_("- The rule expired on %s.") % config.valid_to)

                if config.permited_users and current_user.id not in config.permited_users.ids:
                    config_errors.append(_("- Your user is not assigned the permissions to apply this discount percentage."))

                if config.permited_customers and line.order_id.partner_id.id not in config.permited_customers.ids:
                    config_errors.append(_("- The customer is not among those allowed by the rule."))

                if config.min_amount > 0 and amount < config.min_amount:
                    config_errors.append(_("- The calculated line amount ($%s) does not reach the minimum ($%s).") % (amount, config.min_amount))

                if not config_errors:
                    is_valid = True
                    break
                else:
                    formatted_errors = '\n'.join(config_errors)
                    all_errors.append(f"Rule: [{config.name}]\n{formatted_errors}")

            if not is_valid:
                error_msg = _(
                    "Could not apply the %s%% discount due to unmet restrictions:\n\n%s"
                ) % (discount, '\n\n'.join(all_errors))
                
                raise ValidationError(error_msg)

    @api.constrains('increment', 'product_id', 'product_uom_qty', 'price_unit')
    def _check_advanced_increment(self):
        for line in self:
            increment = line.increment
            if not increment or line.display_type:
                continue

            configs = self.env['increment.line.configuration'].search([('increment', '=', increment)])
            if not configs:
                raise ValidationError(
                    _("The %s%% increment is not part of the rules permitted by the business.") % increment
                )

            today = fields.Date.context_today(line)
            current_user = self.env.user
            
            product_template_id = line.product_id.product_tmpl_id.id if line.product_id else False
            qty = line.product_uom_qty
            price = line.price_unit
            amount = qty * price

            is_valid = False
            all_errors = []

            for config in configs:
                config_errors = []

                if config.permited_products and product_template_id not in config.permited_products.ids:
                    config_errors.append(_("- The product is not among those allowed by the rule."))

                if config.valid_from and today < config.valid_from:
                    config_errors.append(_("- Rule valid only from %s.") % config.valid_from)
                if config.valid_to and today > config.valid_to:
                    config_errors.append(_("- The rule expired on %s.") % config.valid_to)

                if config.permited_users and current_user.id not in config.permited_users.ids:
                    config_errors.append(_("- Your user is not assigned the permissions to apply this increment percentage."))

                if config.permited_customers and line.order_id.partner_id.id not in config.permited_customers.ids:
                    config_errors.append(_("- The customer is not among those allowed by the rule."))

                if config.min_amount > 0 and amount < config.min_amount:
                    config_errors.append(_("- The calculated line amount ($%s) does not reach the minimum ($%s).") % (amount, config.min_amount))

                if not config_errors:
                    is_valid = True
                    break
                else:
                    formatted_errors = '\n'.join(config_errors)
                    all_errors.append(f"Rule: [{config.name}]\n{formatted_errors}")

            if not is_valid:
                error_msg = _(
                    "Could not apply the %s%% increment due to unmet restrictions:\n\n%s"
                ) % (increment, '\n\n'.join(all_errors))
                
                raise ValidationError(error_msg)