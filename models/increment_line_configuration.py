from odoo import models, fields

class IncrementLineConfiguration(models.Model):
    """
    Configuration model to define rules and restrictions for applying specific price increments.
    """
    _name = 'increment.line.configuration'
    _description = 'Increment Line Configuration'

    name = fields.Char(string="Name", required=True, help="Identifying name for the rule.")
    increment = fields.Float(string="Increment (%)", required=True, digits='Discount')
    # If set, the increment only applies to these products
    permited_products = fields.Many2many('product.template', string="Permitted Products")
    # Date range for the rule's validity
    valid_from = fields.Date(string="Valid From")
    valid_to = fields.Date(string="Valid To")
    # If set, only these users can apply the increment
    permited_users = fields.Many2many('res.users', string="Permitted Users")
    # If set, only these customers can receive the increment
    permited_customers = fields.Many2many('res.partner', string="Permitted Customers")
    # Minimum line amount required to apply the increment
    min_amount = fields.Float(string="Minimum Amount (Value)", digits='Product Price')
    active = fields.Boolean(default=True, string="Active", help="If unchecked, it will allow you to hide the rule without removing it.")
