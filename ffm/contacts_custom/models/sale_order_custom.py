from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
class SaleOrderline(models.Model):
    _inherit = 'sale.order.line'

    reason = fields.Selection(string='Reason',selection=[('near_expiry', 'Near Expiry'), ('promotion', 'Promotion'),
             ('key_account', 'Key Account'),('other', 'Other')])

    @api.onchange("product_uom_qty")
    def onchange_product_uom_qty(self):
        # result =(SaleOrderline, self).onchange_product_uom_qty()
        if self.product_uom_qty <= 0:
            raise ValidationError("Error")
        # return result

    approve_name = fields.Boolean("approve")

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderline, self).product_id_change()
        if self.order_id.is_waiting_for_approval == True:
            self.approve_name = True

        else:
            if self.order_id.partner_id.id == False:
                raise ValidationError("Select Customer")

            checker = self.env['partner.pricing'].search(
                [('partner_id', '=', self.order_id.partner_id.id), ('product_id', '=', self.product_id.id)])

            if checker:
                raise ValidationError("A Product That Has Already Been Quoted Cannot Be Quoted Again")
        return res
