{
    'name': 'FFM CRM',
    'version': '1.1',
    'summary': 'FFM CRM',
    'sequence': 1,
    'depends': ['sale', 'stock', 'base', 'web_google_maps'],
    'data': [
        'security/ir.model.access.csv',
        #'views/crm_contact_information.xml',
        # 'views/map_view.xml',
        'views/contacts_informations.xml',
        ],
    "images": ['static/description/icon.png'],
    'application': True,
    'installable': True,
}