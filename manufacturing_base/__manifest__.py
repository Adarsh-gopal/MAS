# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Base Odoo 14",

    'summary': """
        Manufacturing Base Odoo 14""",

    'description': """
        Manufacturing Base
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",

    'category': 'Manufacturing',
    'version': '14.0.1.3',

    'depends': ['mrp'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/mrp_bom_operation.xml',
        'views/item_group.xml',
    ],
}
