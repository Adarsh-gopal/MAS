# -*- coding: utf-8 -*-
{
    'name': "Stock Account Base",

    'summary': """
        Stock Account Base""",

    'description': """
       1) Access control to open revaluation screen .
       2) No create and edit of GL selection
       3) Mandatory of Reason field
       4) Added a new feild called Lamded Cost Name
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "http://www.prixgen.com",

    'category': 'Inventory',
    'version': '14.0.1.3',

    'depends': ['stock_account','stock_landed_costs'],

    'data': [
        'views/stock_valuation_layer.xml'
    ],
}