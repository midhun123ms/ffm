from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError,ValidationError
import datetime
from lxml import etree
from odoo.tools.misc import formatLang, get_lang


class QuotationStatus(models.Model):

    _inherit ='sale.order'

    # state = fields.Selection(selection_add=[('approval', 'Approval')])
    is_waiting_for_approval = fields.Boolean("Is Waiting for Approval", default=False)
    type_customer = fields.Char(string="Type")
    date_order = fields.Datetime(string='Sale Order Date', required=True, readonly=True, index=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
                                 default=fields.Datetime.now,
                                 help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    # date_date = fields.Datetime(string='Sale Order Date', required=True, index=True, default=fields.Datetime.now)

    state = fields.Selection([
        ('sdraft', 'Draft'),
        ('draft', 'Draft'),
        ('sent', 'Quotation Sent'),
        ('WaitingForApproval', 'Waiting for Approval'),
        ('quotation', 'Quotations'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('approval', 'Approval'),
        ('cancel', 'Cancelled'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),

    ], string='Status', readonly=True, copy=False, index=False, tracking=None)




    # def create(self, state):
    #     res = super(QuotationStatus, self).create(state)
    #     res.state = 'SaleDraft'
    #     return res
    # def customer_type(self):
    #     if self.type_customer:
    #         self.type_customer = self.env['account.move.line'].search([('type_customer', '=', '')

    def action_waiting_for_approve(self):
        if self.state:
            self.state = "WaitingForApproval"

        # for val in self.order_line:
        #     pricing = self.env['partner.pricing'].search(
        #         [('partner_id', '=', self.partner_id.id), ('product_id', '=', val.product_id.id)])
        #     # if pricing:
        #     #     self.env['partner.pricing'].price = self.env['sale.order.line'].val.price_unit
        #     if not pricing:
        #         self.env['partner.pricing'].create({
        #             'partner_id': self.partner_id.id,
        #             'product_id': val.product_id.id,
        #             'price': val.price_unit})
        #     else:
        #         if not self.order_line:
        #             raise UserError(("No quotation for product."))

        # for val in self.order_line:
        #     price_unit_check = self.env['partner.pricing'].search(
        #         [('partner_id', '=', self.partner_id.id), ('product_id', '=', val.product_id.id)])
        #     if not price_unit_check:
        #         raise UserError(_("No quotation for product."))

    def action_approve(self):
        # res = super(QuotationStatus, self).action_confirm()
        if self.state:
            self.state = "quotation"

        for val in self.order_line:
            pricing = self.env['partner.pricing'].search(
                [('partner_id', '=', self.partner_id.id), ('product_id', '=', val.product_id.id)])
            # if pricing:
            #     self.env['partner.pricing'].price = self.env['sale.order.line'].val.price_unit

            # if pricing:
            #     pricing.write({
            #         'price': val.price_unit})


            if not pricing:
                self.env['partner.pricing'].create({
                    'partner_id': self.partner_id.id,
                    'product_id': val.product_id.id,
                    'price': val.price_unit})
            else:
                if not self.order_line:
                    raise UserError(("No quotation for product."))

    # @api.model
    # def create(self, vals):
    #     res = super(QuotationStatus, self).create(vals)
    #     for val in vals['order_line']:
    #         pricing = self.env['partner.pricing'].search([('partner_id', '=', vals['partner_id'])])
    #         if pricing:
    #             self.env['partner.pricing'].create({
    #                 'partner_id': vals['partner_id'],
    #                 'product_id': val[2]['product_id'],
    #                 'price': val[2]['price_unit']})
    #     return res


    # def write(self, vals):
    #     res = super(QuotationStatus, self).write(vals)
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@", vals)
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@", vals['order_line'])
    #     for val in vals['order_line']:
    #         print("--------------------", val)
    #         print("!!!!!!!!!!!!!!!!!!!", self.partner_id.id)
    #         print("+++++++++++++++++++", vals['product_id'])
    #         # print("!!!!!!!!!!!!!!!!!!!", val[2]['price_unit'])
    #         # pricing = self.env['partner.pricing'].search(
    #         #     [('partner_id', '=', self.partner_id.id), ('product_id', '=', val[2]['product_id'])])
    #         # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #         # print("!!!!!!!!!!!!!!!!!!!", self.partner_id.id)
    #         # print("!!!!!!!!!!!!!!!!!!!",  val[2]['product_id'])
    #         # print("!!!!!!!!!!!!!!!!!!!", val[2]['price_unit'])
    #         # self.env['partner.pricing'].create({
    #         #     'partner_id': self.partner_id.id,
    #         #     'product_id': val[2]['product_id'],
    #         #     'price': val[2]['price_unit']})
    #         # print("///////////////")
    #         # else:
    #         #     if not vals['order_line']:
    #         #         raise UserError(("No quotation for product."))
    #     return res



    @api.onchange('partner_id')
    def on_change_type_customer(self):
        if self.partner_id:
            cust_type = self.partner_id.customer_type
            pymnt_term = self.partner_id.property_payment_term_id
            self.payment_term_id = pymnt_term
            self.type_customer = cust_type

    def action_confirm(self):
        res = super(QuotationStatus, self).action_confirm()
        # print("python recursive limit",sys.getrecursionlimit())
        if self.type_customer == 'cash':
            move_line = self.env['account.move.line'].search(
                [('move_id.state', '=', 'posted'), ('partner_id', '=', self.partner_id.id),
                 ('account_id', '=', self.partner_id.property_account_receivable_id.id)])
            total_debit = 0.0
            total_credit = 0.0
            for val in move_line:
                total_debit += val.debit
                total_credit += val.credit
            if total_debit - total_credit > 0:
                # raise UserError("Customer have pending dues.")
                self.state = 'approve'
            else:
                self.state = 'sale'

        if self.type_customer == 'credit':
            if not self.date_order:
                raise UserError("Please fill invoice date.")
            else:
                date = self.date_order
                first = date.replace(day=1)
                lastMonth = first - datetime.timedelta(days=1)

                move_line_last_month = self.env['account.move.line'].search(
                    [('move_id.state', '=', 'posted'), ('date', '<=', lastMonth),
                     ('partner_id', '=', self.partner_id.id),
                     ('account_id', '=', self.partner_id.property_account_receivable_id.id)])

                move_line_till_date = self.env['account.move.line'].search(
                    [('move_id.state', '=', 'posted'), ('partner_id', '=', self.partner_id.id),
                     ('account_id', '=', self.partner_id.property_account_receivable_id.id)])

                last_month_total_debit = 0.0

                for val in move_line_last_month:
                    last_month_total_debit += val.debit

                total_credit = 0.0
                total_debit = 0.0
                for val in move_line_till_date:
                    total_credit += val.credit
                    total_debit += val.debit

                if last_month_total_debit - total_credit > 0:

                    # raise UserError("Customer have last month pending dues.")
                    self.state = 'approve'
                else:
                    if total_debit - total_credit > self.partner_id.credit_limit:
                        # raise UserError("Credit limit exceeded.")
                        self.state = 'approve'
                    else:
                        # return self._post(soft=False)
                        self.state = 'sale'

        for val in self.order_line:
            pricing = self.env['partner.pricing'].search(
                [('partner_id', '=', self.partner_id.id), ('product_id', '=', val.product_id.id)])
            if pricing:
                # print("***************", self.partner_id.pricing_ids.price)
                va = pricing.price
                if val.price_unit < va:
                    lister = []
                    lister.append(val.product_id.name)
                    print("................", lister)
                    # mystring = ''.joining(map(str, lister))
                    raise ValidationError(_("The Price Is Less"))
        return res


    def action_approve_button(self):
        return self.write({'state': 'sale'})


    def action_reject_button(self):
        return self.write({'state': 'reject'})


    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(QuotationStatus, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                           submenu=submenu)
        doc = etree.XML(res['arch'])
        # print("############doc",doc)
        # print("############self.partner_id.active",self.partner_id)
        active_id = self._context.get('active_ids')
        active_object = self.env['res.partner'].search([('id', '=', active_id)])
        print("testtttttttt", active_id)
        if active_id:
            if view_type == 'tree' and active_object.active is False:
                for node_form in doc.xpath("//tree"):
                    node_form.set("create", 'false')
                    res['arch'] = etree.tostring(doc)
        return res


class SaleOrderLineInherited(models.Model):

    _inherit = "sale.order.line"


    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLineInherited, self).product_id_change()
        self.name = self.product_id.description_sale
        return res

    # @api.onchange('product_id')
    # def price_id_change(self):
    #     res = super(SaleOrderLine, self).product_id_change()
    #     if self.order_id.is_waiting_for_approval == True:
    #         self.approve_name = True
    #         print(":::::::::::::::::", self.approve_name)
    #     return res

