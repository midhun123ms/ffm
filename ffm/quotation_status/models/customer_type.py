# from odoo import api, models, fields, _
# from odoo.exceptions import AccessError, UserError, ValidationError
# import datetime
#
# class AccountMove(models.Model):
#     _inherit = "res.partner"
#
#     customer_type = fields.Selection([('credit', 'Credit'), ('cash', 'Cash')], string="Type")
#     property_payment_term_id = fields.Many2one('account.payment.term', company_dependent=True,
#                                                string='Customer Payment Terms', required=1,
#                                                domain="[('company_id', 'in', [current_company_id, False])]",
#                                                help="This payment term will be used instead of the default one for sales orders and customer invoices")

    # def action_post(self):
    #     if self.customer_type == 'cash':
    #         move_line = self.env['account.move.line'].search([('move_id.state', '=', 'posted'),('partner_id','=',self.partner_id.id),('account_id','=',self.partner_id.property_account_receivable_id.id)])
    #         total_debit = 0.0
    #         total_credit = 0.0
    #         for val in move_line:
    #             total_debit += val.debit
    #             total_credit += val.credit
    #         if total_debit - total_credit > 0:
    #             raise UserError(_("Customer have pending dues."))
    #         else:
    #             return self._post(soft=False)
    #
    #     if self.customer_type == 'credit':
    #         if not self.invoice_date:
    #             raise UserError(_("Please fill invoice date."))
    #         else:
    #             date = self.invoice_date
    #             first = date.replace(day=1)
    #             lastMonth = first - datetime.timedelta(days=1)
    #
    #             move_line_last_month = self.env['account.move.line'].search([('move_id.state', '=', 'posted'),('date', '<=', lastMonth), ('partner_id', '=', self.partner_id.id),
    #                                     ('account_id', '=', self.partner_id.property_account_receivable_id.id)])
    #
    #             move_line_till_date = self.env['account.move.line'].search([('move_id.state', '=', 'posted'),('partner_id','=',self.partner_id.id),
    #                                   ('account_id','=',self.partner_id.property_account_receivable_id.id)])
    #
    #             last_month_total_debit = 0.0
    #             for val in move_line_last_month:
    #                 last_month_total_debit += val.debit
    #
    #             total_credit = 0.0
    #             total_debit = 0.0
    #             for val in move_line_till_date:
    #                 total_credit += val.credit
    #                 total_debit += val.debit
    #
    #             if last_month_total_debit - total_credit > 0:
    #                 raise UserError(_("Customer have last month pending dues."))
    #
    #             else:
    #                 if total_debit - total_credit > self.partner_id.credit_limit:
    #                     raise UserError(_("Credit limit exceeded."))
    #                 else:
    #                     return self._post(soft=False)
    #

