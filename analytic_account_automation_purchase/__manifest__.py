# -*- coding: utf-8 -*-
{
    'name': "Analytic Account For Purchase for MAS",

    'summary': """
        Analytic Account For Purchase""",

    'description': """
        Analytic Account For Purchase
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': "https://www.prixgen.com",

    'category': 'Accounting',
    'version': '14.0.1.8',

    'depends': ['purchase','stock_landed_costs',
                'analytic_account_automation_accounts',
                'analytic_account_automation_inventory'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_order.xml',
        'views/stock_picking.xml',
        'views/landed_cost.xml',
    ],
}
