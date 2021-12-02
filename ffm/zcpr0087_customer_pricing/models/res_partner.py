from odoo import api, models, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pricing_ids = fields.One2many('partner.pricing', 'partner_id', string="Pricing")
    credit_limit = fields.Float(string="Credit Limit")




    # @api.onchange('pricing_ids')
    # def line_id_pricing(self):
    #     print("sssssssssssssssssssss")
    #     if self.name:
    #         print("gggggggggg", self.name)
    #         print("ffffffffff", self.name.id)


    # print("222222222222222222")
    # def write(self, vals):
    #     print("1111111111111111111111111")
    #     res = super(ResPartners, self).write(vals)
    #     print("########################")
    #     if self.name:
    #         # pricing_ids = fields.One2many('partner.pricing', 'partner_id', string="Pricing", readonly=True, pad_no_create=True)
    #         product_id = fields.Many2one('product.product', string="Product", readonly=True)
    #         price = fields.Float(string="Price", readonly=True)
    #     print("**************************")
    #     return res