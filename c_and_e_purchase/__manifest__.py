{
    'name': 'Create and edit restriction for purchase',
    'version': '14.0.3',
    'description': """This module consists, the product creating and editing restriction in 
                   Purchase""",
    'category': 'Purchase',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['purchase','purchase_requisition','purchase_base_14'],
    'data': [   
        'views/purchase_restriction.xml',   
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
