from odoo import models, fields

class DiscountApprovalChain(models.Model):
    _name = 'discount.approval.chain'
    _description = 'Discount Approval Chain'
    _order = 'min_percent asc'

    name = fields.Char('Name', required=True)
    min_percent = fields.Float('Min Discount (%)', required=True)
    max_percent = fields.Float('Max Discount (%)', required=True)
    approver_id = fields.Many2one('res.users', 'Approver User', required=True)
