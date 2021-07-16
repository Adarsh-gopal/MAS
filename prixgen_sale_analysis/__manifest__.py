# -*- coding: utf-8 -*-
{
    'name': "Sale Analysis",

    'summary': """
        Sale Analysis""",

    'description': """
    Included Feature
        1. Group by based on product category,
        2. Group by based on product ,
        3. Group by based on sales person,
        4. Group by based on sales team,
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",


    'category': 'Customization',
    'version': '14.0.1',

    'depends': ['account_base'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_analysis_report.xml',
    ],
    'auto_install': False,
    'installable': True,
}
