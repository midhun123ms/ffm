{
    'name' : 'product_change',
    'version' : '1.0',
    'summary': 'product_change',
    'sequence': 9,
    'description': """ product_changing""",
    'category': 'product_change',
    'website': 'www.odoo.com',
    'images': [],
    'depends' : ['base', 'sale_management'],
    'data': ['views/product_changing.xml',
             'security/ir.model.access.csv'
             ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
