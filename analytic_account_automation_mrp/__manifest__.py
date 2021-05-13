# -*- coding: utf-8 -*-
{
    'name': "Analytic Account For Manufacturing for MAS",

    'summary': """
        Analytic Account For Manufacturing""",

    'description': """
        Analytic Account For Manufacturing
    """,

    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',

    'category': 'Accounting',
    'version': '14.0.1.4',

    'depends': ['account',
                'stock',
                'mrp',
                'analytic_account_automation_accounts',
                'analytic_account_automation_inventory'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/mrp_production.xml',
    ],
}
