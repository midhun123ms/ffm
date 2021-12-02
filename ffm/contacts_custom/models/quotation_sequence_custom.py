from odoo import api, fields, models, SUPERUSER_ID, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
    #                    states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    @api.depends('order_line.discount')
    def _amount_discount(self):
        for order in self:
            amount_discount = 0.0
            for line in order.order_line:
                # disc_quantity =
                amount_amount = line.price_unit * ((line.discount or 0.0) / 100.0)*line.product_uom_qty
                print("************", amount_amount)
                amount_discount += amount_amount
                print("------------------", amount_discount)
            order.update({
                'amount_discount': amount_discount,
            })


    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_discount')

    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
                a = self.is_waiting_for_approval
                # print(a)
                if a == False:
                    # vals['name'] = self.env['ir.sequence'].next_by_code('sale.order', sequence_date=seq_date) or _('New')
                    vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.quotation', sequence_date=seq_date) or _('New')
                else:
                    vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.sequence', sequence_date=seq_date) or _('New')


        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist.id)
        result = super(SaleOrder, self).create(vals)
        return result