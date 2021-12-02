from odoo import api, models, fields, _
from odoo.tools.misc import formatLang, get_lang
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('approval', 'Approval')])




    def action_confirm(self):
        #Margin Approval
        approval = []
        for val in self.order_line:
            if val.product_id.standard_price > 0:
                margin = val.price_unit - val.product_id.standard_price
                value = (margin / val.product_id.standard_price) * 100
                if value < 23:
                    approval.append(value)

        if self.state == 'draft' and len(approval) > 0:
            self.state = 'approval'

        else:
            self.state = 'approval'
            #Customer Wise Pricing
            for val in self.order_line:
                pricing = self.env['partner.pricing'].search([('partner_id','=', self.partner_id.id),('product_id','=',val.product_id.id)])
                if not pricing:
                    self.env['partner.pricing'].create({
                                                    'partner_id':self.partner_id.id,
                                                    'product_id':val.product_id.id,
                                                    'price':val.price_unit})
            if self._get_forbidden_state_confirm() & set(self.mapped('state')):
                raise UserError(_(
                    'It is not allowed to confirm an order in the following states: %s'
                ) % (', '.join(self._get_forbidden_state_confirm())))

            for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
                order.message_subscribe([order.partner_id.id])
            self.write(self._prepare_confirmation_values())

            # Context key 'default_name' is sometimes propagated up to here.
            # We don't need it and it creates issues in the creation of linked records.
            context = self._context.copy()
            context.pop('default_name', None)
            context['default_state'] ='draft'
            self.with_context(context)._action_confirm()
            if self.env.user.has_group('sale.group_auto_done_setting'):
                self.action_done()

    def _action_cancel(self):
        result = super(SaleOrder, self)._action_cancel()
        self.context['default_state'] = 'draft'
        return result


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    def _get_display_price(self, product):
        #Customer Wise Pricing
        pricing = self.env['partner.pricing'].search([('partner_id','=',self.order_id.partner_id.id),('product_id','=',product.id)])
        if pricing:
            final_price = pricing.price
            return final_price
        else:
            # TO DO: move me in master/saas-16 on sale.order
            # awa: don't know if it's still the case since we need the "product_no_variant_attribute_value_ids" field now
            # to be able to compute the full price

            # it is possible that a no_variant attribute is still in a variant if
            # the type of the attribute has been changed after creation.
            no_variant_attributes_price_extra = [
                ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
                    lambda ptav:
                        ptav.price_extra and
                        ptav not in product.product_template_attribute_value_ids
                )
            ]
            if no_variant_attributes_price_extra:
                product = product.with_context(
                    no_variant_attributes_price_extra=tuple(no_variant_attributes_price_extra)
                )

            if self.order_id.pricelist_id.discount_policy == 'with_discount':
                return product.with_context(pricelist=self.order_id.pricelist_id.id).price
            product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)

            final_price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(product or self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
            base_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)
            if currency != self.order_id.pricelist_id.currency_id:
                base_price = currency._convert(
                    base_price, self.order_id.pricelist_id.currency_id,
                    self.order_id.company_id or self.env.company, self.order_id.date_order or fields.Date.today())
            # negative discounts (= surcharge) are included in the display price
            return max(base_price, final_price)
