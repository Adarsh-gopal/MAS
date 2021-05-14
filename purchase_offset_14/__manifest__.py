# -*- coding: utf-8 -*-
{
    'name': "Purchase Offset 14",

    'summary': """
        Purchase Offset Base App for Odoo 14""",

    'description': """
        On posting of Vendor Bill add purchase and purchase offset account entries to journal items
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "http://www.prixgen.com",

    'category': 'Accounting',
    'version': '14.0.1.6',

    'depends': ['base','product','account','account_accountant'],

    'data': [
        'views/account.xml'
    ],
}
