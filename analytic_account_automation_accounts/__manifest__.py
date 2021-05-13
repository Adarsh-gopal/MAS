# -*- coding: utf-8 -*-
{
    'name': "Analytic Account For Accounts for MAS",

    'summary': """
        Analytic Account For Accounts""",

    'description': """
        Analytic Account For Accounts
    """,

    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',

    'category': 'Accounting',
    'version': '14.0.1.8',

    'depends': ['account','account_accountant','base'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/payment.xml',
        'views/account_move.xml',
        'views/res_company.xml'
    ],
}
