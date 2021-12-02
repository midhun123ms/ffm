from odoo import api, fields, models, SUPERUSER_ID, _

class ResBanking(models.Model):
    _inherit = "res.bank"

    acc_no = fields.Char(string="Account Number", required=True)
    iban = fields.Char(string="IBAN", required=True)
    swift = fields.Char(string="Swift", required=True)
    acc_name = fields.Char(string="Account Holder Name", required=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company, ondelete='cascade', readonly=True)


