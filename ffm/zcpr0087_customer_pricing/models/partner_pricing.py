from odoo import api, models, fields, _


class PartnerPricing(models.Model):
    _name = 'partner.pricing'
    _description = "Pricing"

    partner_id = fields.Many2one('res.partner', string="Partner")
    product_id = fields.Many2one('product.product', string="Product")
    price = fields.Float(string="Price")

