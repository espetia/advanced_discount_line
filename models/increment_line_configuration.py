from odoo import models, fields

class IncrementLineConfiguration(models.Model):
    _name = 'increment.line.configuration'
    _description = 'Increment Line Configuration'

    name = fields.Char(string="Name", required=True, help="Identifying name for the rule.")
    increment = fields.Float(string="Increment (%)", required=True, digits='Discount')
    permited_products = fields.Many2many('product.template', string="Permitted Products")
    valid_from = fields.Date(string="Valid From")
    valid_to = fields.Date(string="Valid To")
    permited_users = fields.Many2many('res.users', string="Permitted Users")
    permited_customers = fields.Many2many('res.partner', string="Permitted Customers")
    min_amount = fields.Float(string="Minimum Amount (Value)", digits='Product Price')
    active = fields.Boolean(default=True, string="Active", help="If unchecked, it will allow you to hide the rule without removing it.")
