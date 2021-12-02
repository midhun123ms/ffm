from odoo import api, models, fields, _
from odoo.exceptions import AccessError, UserError, ValidationError
import datetime

class AccountMove(models.Model):
    _inherit = "account.move"

    customer_type = fields.Selection([('credit', 'Credit'), ('cash', 'Cash')], string="Type")
    # customer_type = fields.Char(string="Type")

    @api.depends('line_ids.discount')
    def _invoice_discount(self):
        for move in self:
            amount_discount = 0.0
            for line in move.line_ids:
                amount_amount = line.price_unit * ((line.discount or 0.0) / 100.0)*line.quantity
                print("//////////////", amount_amount)
                amount_discount += amount_amount
                print("+++++++++++++++", amount_discount)
            move.update({
                'amount_discount': amount_discount,
            })

    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_invoice_discount')

    def action_post(self):
        if self.customer_type == 'cash':
            move_line = self.env['account.move.line'].search([('move_id.state', '=', 'posted'),('partner_id','=',self.partner_id.id),('account_id','=',self.partner_id.property_account_receivable_id.id)])
            total_debit = 0.0
            total_credit = 0.0
            for val in move_line:
                total_debit += val.debit
                total_credit += val.credit
            if total_debit - total_credit > 0:
                raise UserError(_("Customer have pending dues."))
            else:
                return self._post(soft=False)

        if self.customer_type == 'credit':
            if not self.invoice_date:
                raise UserError(_("Please fill invoice date."))
            else:
                date = self.invoice_date
                first = date.replace(day=1)
                lastMonth = first - datetime.timedelta(days=1)

                move_line_last_month = self.env['account.move.line'].search([('move_id.state', '=', 'posted'),('date', '<=', lastMonth), ('partner_id', '=', self.partner_id.id),
                                        ('account_id', '=', self.partner_id.property_account_receivable_id.id)])

                move_line_till_date = self.env['account.move.line'].search([('move_id.state', '=', 'posted'),('partner_id','=',self.partner_id.id),
                                      ('account_id','=',self.partner_id.property_account_receivable_id.id)])

                last_month_total_debit = 0.0
                for val in move_line_last_month:
                    last_month_total_debit += val.debit

                total_credit = 0.0
                total_debit = 0.0
                for val in move_line_till_date:
                    total_credit += val.credit
                    total_debit += val.debit

                if last_month_total_debit - total_credit > 0:
                    raise UserError(_("Customer have last month pending dues."))

                else:
                    if total_debit - total_credit > self.partner_id.credit_limit:
                        raise UserError(_("Credit limit exceeded."))
                    else:
                        return self._post(soft=False)


    @api.onchange('partner_id')
    def on_change_customer_type(self):
        if self.partner_id:
            type_cust = self.partner_id.customer_type
            self.customer_type = type_cust
            payment_term = self.partner_id.property_payment_term_id
            self.invoice_payment_term_id = payment_term


    # @api.depends('customer_type')
    # def _compute_customer_type_id(self):
    #     if self.partner_id:
    #         type_cust = self.partner_id.customer_type
    #         self.customer_type = type_cust