# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Contacts Custom',
    'version': '1.1',
    'summary': 'Contacts Customisation',
    'depends': ['base','account','stock','sale','purchase','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/contact_custom.xml',
        'views/product_line_readonly.xml',
        'views/preview_form.xml',
        'views/sale_order_custom.xml',
        ],

    "images": ['static/description/icon.png'],
    'application': False,
    'installable': True,

}
