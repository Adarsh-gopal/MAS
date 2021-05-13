# -*- coding: utf-8 -*-
{
    'name': "Analytic Account For Inventory Odoo14 for MAS",

    'summary': """
        Analytic Account For Inventory""",

    'description': """
        Analytic Account For Inventory
    """,

    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',

    'category': 'Accounting',
    'version': '14.0.1.5',

    'depends': ['stock','stock_account','analytic_account_automation_accounts'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking.xml',
        'views/stock_inventory.xml',
    ],
}
