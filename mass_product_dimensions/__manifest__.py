# -*- coding: utf-8 -*-
{
    'name': 'Mas Product Dimension',
    'version': '14.0.2',
    'category': 'Customization',
    'description': """
This module adds product dimensions
""",
	'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': [
        'product',
        'sale',
        'web',
        'mass_product_specifications',
    ],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'application': False,
    'installable': True,
}
