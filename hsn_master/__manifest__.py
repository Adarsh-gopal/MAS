{
    'name': 'HSN Master',
    'version': '14.0.1',
    'category': 'Inventory',
    
    'summary': 'HSN Master',
    'description': " HSN  Master",
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",
    'depends': ['base','stock','l10n_in'],
    'data': [
    'security/ir.model.access.csv',
    'views/hsn.xml',
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False
}
