# -*- coding: utf-8 -*-
{
    'name': "Mrp Subcontract Menu",

    'summary': """
        Additional menu for sub-contracts orders""",

    'description': """
	    Upon clicking the Sub con Order menu, it shows the orders whose operation_type_name is Subcontract.
    """,

    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com', 

    'category': 'Customization',
    'version': '14.0.10',


    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
