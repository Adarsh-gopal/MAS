# -*- coding: utf-8 -*-
{
    'name': "Inventory Base Summary",

    'summary': """
        Inventory Base Summary""",

    'description': """
        Inventory Base Summary
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "http://www.prixgen.com",

    'category': 'Inventory',
    'version': '14.0.2.16',

    'depends': ['base','product','stock','stock_account','inventory_base'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
