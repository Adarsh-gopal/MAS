# -*- coding: utf-8 -*-
{
    'name': "Inventory Aging Report Odoo 14",

    'summary': """
        Inventory Aging Report for Odoo 14 Enterprise Edition
        """,

    'description': """
        Inventory Aging Report for Odoo 14 Enterprise Edition
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "http://www.prixgen.com",

    'category': 'Inventory',
    'version': '14.0.2.1',

    'depends': ['base','stock','sale','sale_management','purchase','account','account_accountant'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}