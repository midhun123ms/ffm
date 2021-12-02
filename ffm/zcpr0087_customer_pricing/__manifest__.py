# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Customer Pricing',
    'version': '1.0',
    'summary': 'Customer Pricing Module',
    'author': 'Zinfog Codelabs',
    'website': 'https://zinfog.com',
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/account_move.xml',
        ],
    'application': False,
    'installable': True,

}
