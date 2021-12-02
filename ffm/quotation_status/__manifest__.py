{
    'name': 'Quotation Status',
    'version': '1.1',
    'summary': 'Quotation status',
    'sequence': 1,
    'depends': ['sale','stock','base','zcpr0087_customer_pricing'],
    'data': [
        'security/ir.model.access.csv',
        'security/manager_access.xml',
        'views/quotation_status.xml',
        # 'views/customer_type.xml',
        ],
    "images": ['static/description/icon.png'],
    'application': True,
    'installable': True,

}