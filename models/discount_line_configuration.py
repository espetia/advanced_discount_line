from odoo import models, fields

class DiscountLineConfiguration(models.Model):
    _name = 'discount.line.configuration'
    _description = 'Discount Line Configuration'

    name = fields.Char(string="Name", required=True, help="Identifying name for the rule.")
    discount = fields.Float(string="Discount (%)", required=True, digits='Discount')
    permited_products = fields.Many2many('product.template', string="Permitted Products")
    valid_from = fields.Date(string="Valid From")
    valid_to = fields.Date(string="Valid To")
    permited_users = fields.Many2many('res.users', string="Permitted Users")
    min_amount = fields.Float(string="Minimum Amount (Value)", digits='Product Price')
