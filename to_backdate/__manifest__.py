{
    'name': "Backdate Operations Access Rights",

    'summary': """
Access group for backdate operations""",
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com', 

    'category': 'Hidden',
    'version': '14.0.1',

    
    'depends': ['base'],

    
    'data': [
        'security/module_security.xml',
        'wizard/abstract_inventory_backdate_wizard_views.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
