# -*- coding: utf-8 -*-
# Copyright 2019 Openworx
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import qrcode
import base64
from io import BytesIO
from odoo import models, fields, api
from odoo.http import request
from odoo import exceptions, _
from datetime import datetime, date

class QRCodeInvoice(models.Model):
    _inherit = 'account.move'

    qr_image = fields.Binary("QR Code", compute='_generate_qr_code')

    total_discount = fields.Float(compute="get_total_discount_lines")

    def get_total_discount_lines(self):
        for rec in self:
            total = 0.0
            for line in rec.invoice_line_ids:
                if line.discount:
                    total += line.price_unit * line.discount / 100
                    rec.total_discount = total
                else:
                    rec.total_discount = 0.0

#    @api.one
    def _generate_qr_code(self):
        service = 'BCD'
		#Check if BIC exists: version 001 = BIC, 002 = no BIC
        if self.company_id.iban_qr_number.bank_id.bic:
            version = '001'
        else:
            version = '002'
        code    = '1'
        function = 'SCT'
        amount_untaxed = str(self.amount_untaxed)
        amount_untaxed = ''.join(['Amount untaxed :  ',str(self.amount_untaxed),' ',self.currency_id.name])
        amount_tax = str(self.amount_tax)
        amount_tax = ''.join(['Amount tax :  ',str(self.amount_tax),' ',self.currency_id.name])
        amount_total = str(self.amount_total)
        amount_total = ''.join(['Amount Total :   ',str(self.amount_total),' ',self.currency_id.name])

        bic =  self.company_id.iban_qr_number and self.company_id.iban_qr_number.bank_id.bic or ''
        company =''.join(['Company Name :  ',self.company_id.name])
        vat =''.join(['Company Vat ID :  ',self.company_id.vat])
        iban =  self.company_id.iban_qr_number and self.company_id.iban_qr_number.acc_number.replace(' ','') or ''
        currency = ''.join([self.currency_id.name, str(self.amount_residual)])
        reference = ''.join(['Invoice Number :  ', str(self.name)])
        lf ='\n'
        ibanqr = lf.join([company,vat,reference,amount_untaxed,amount_tax,amount_total,])
        print(ibanqr)
        if len(ibanqr) > 331:
            raise exceptions.except_orm (_('Error'), _('IBAN QR code "%s" length %s exceeds 331 bytes') % (ibanqr, len(ibanqr)))
        self.qr_image = generate_qr_code(ibanqr)

def generate_qr_code(value):
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
    )
    qr.add_data(value)
    qr.make(fit=True)
    img = qr.make_image()
    temp = BytesIO()
    img.save(temp, format="PNG")
    qr_img = base64.b64encode(temp.getvalue())
    return qr_img



class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    tax_amount = fields.Float(string="Tax Amount", compute="_compute_tax_amount")


    @api.depends('tax_ids', 'price_unit','quantity')
    def _compute_tax_amount(self):
        for line in self:
            if line.tax_ids:
                line.tax_amount = line.price_total - line.price_subtotal
            else:
                line.tax_amount = 0.0