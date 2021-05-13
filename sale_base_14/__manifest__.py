# -*- coding: utf-8 -*-
{
    'name': "Sale Base Odoo 14",

    'summary': """
        Sale Base Odoo 14""",

    'description': """
        Sale Base Odoo 14
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "http://www.prixgen.com",

    'category': 'Sale',
    'version': '14.0.1.3',

    'depends': ['base','sale','inventory_base','account'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml'
    ],
}
