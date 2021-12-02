from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.order_id.is_waiting_for_approval == True:
            product_ids = []
            for rec in self.order_id.partner_id.pricing_ids:
                product_ids.append(rec.product_id.id)
            domain = {'product_id': [('id', 'in', product_ids)]}
            return {'domain': domain}
        return res


class Trace(models.Model):
    _inherit = 'res.partner'


    mid_n = fields.Char(string="Middle Name")
    lst_n = fields.Char(string="Last Name", required=True)
    function = fields.Selection(
        [('purchase_manager', 'Purchase Manager'),
         ('ops_manager', 'Ops Manager'),
         ('owner', 'Owner'),
         ('chef', 'Chef'),
         ('accountant', 'Accountant'),
         ('other', 'Other'),
        ], string='Job Position', default='purchase_manager', required=True)

    acc_for = fields.Many2many('many.master', string='Accountable for', required=True)


    pass_port = fields.Char(string="Passport/ID number")
    mob_one = fields.Char(string="Mobile 2")
    ex_tension = fields.Char(string="Extension")
    pre_language = fields.Many2one('res.lang', string="Preferred Language", required=True)
    age_age = fields.Char(string="Age")


    user_change = fields.Boolean(compute='_compute_user_changes', store=True)

    @api.depends('name')
    def _compute_user_changes(self):
        for rec in self:
            user_pool = rec.env['res.users']
            user = user_pool.browse(rec._uid)
            desired_user_gr = user.has_group('base.user_admin')
            if desired_user_gr:
                rec.user_change = True




class ManyMaster(models.Model):
    _name = 'many.master'

    name = fields.Char()






    # @api.onchange('product_id')
    # def on_change_product_id(self):
    #     product_ids = []
    #     for rec in self.order_id.partner_id.pricing_ids:
    #         product_ids.append(rec.id)
    #     print("#############rec", product_ids)
    #     domain = {'product_id': [('id', 'in', product_ids)]}
    #     return {'domain': domain}



