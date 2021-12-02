# -*- coding: utf-8 -*-
# Copyright 2019, 2021 Openworx
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "E-Invoice For VAT and Zakat in KSA",
    "summary": "E-Invoice For VAT and Zakat in KSA",
    "version": "14.0",
    "price" : "90",
    "currency" : "USD",
    "author": "Osman Alrasheed",
    "website": "https://www.snit.sa",
    'category': 'Accounting',
    "depends": ['base','account','sale_management'],
    "data": [
        'views/invoice_vat_qr.xml',
		'views/res_company_view.xml',
        'reports/report_invoice.xml',
    ],
    "license": "LGPL-3",
    'images': ['images/ibanqr.png'],
    "installable": True,
    "application": False,
}
