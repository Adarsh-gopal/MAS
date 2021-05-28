# -*- coding: utf-8 -*-
{
    'name': "Inventory Detailed Summary",

    'summary': """
        Inventory Detailed Summary""",

    'description': """
        Inventory Detailed Summary
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "http://www.prixgen.com",

    'category': 'Inventory',
    'version': '14.0.2.9',

    'depends': ['base','product','stock','stock_account','inventory_base','sale','sale_stock','purchase','purchase_stock','inventory_balance_summary_14'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}