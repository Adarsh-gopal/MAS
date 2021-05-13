# -*- coding: utf-8 -*-
{
    'name': "Analytic Account For Sales for MAS",

    'summary': """
        Analytic Account For Sales""",

    'description': """
        Analytic Account For Sales
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': 'Prixgen Tech Solutions Pvt Ltd.',
    'website': "https://www.prixgen.com",

    'category': 'Accounting',
    'version': '14.0.1.4',

    'depends': ['sale','sale_stock','analytic_account_automation_inventory'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
    ],
}
