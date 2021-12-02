from odoo import api, fields, models, SUPERUSER_ID, _

class AccountMoving(models.Model):
    _inherit = "account.move"

    def invoice_button(self):
        return self.env.ref('e_tax_invoice_saudi_aio.action_report_tax_invoice').report_action(self)

    bank_id = fields.Many2one('res.bank', string='Bank')


