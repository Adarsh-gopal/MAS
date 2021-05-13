# -*- coding: utf-8 -*-
{
    'name': "Stock Transfers Backdate",
    'summary': """ Manual validation date for stock transfers. """,
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com', 

    'category': 'Warehouse',
    'version': '14.0.1',

    'depends': ['stock_account', 'to_backdate'],

    'data': [
        'security/module_security.xml',
        'wizard/stock_picking_backdate_views.xml'
    ],
    'post_init_hook': 'post_init_hook',
    'application': False,
    'installable': True,
    'license': 'OPL-1',
}
