# -*- coding: utf-8 -*-
{
    'name': 'Mas Product Specification',
    'version': '14.0.3',
    'category': 'Customization',
    'description': """
This module adds product specification
""",
	'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': [
        'product',
        'stock',
        'stock_account',
        'inventory_base',
    ],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'application': False,
    'installable': True,
}
