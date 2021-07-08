# -*- coding: utf-8 -*-
{
    'name': "New Sale Register Report",

    'summary': """
        This module is used to capture Sale Register Report
    """,

    'description': """ 
        This module is used to capture the Sale Register Report
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "http://www.prixgen.com",

    'category': 'Sale',
    'version': '14.0.7',

    'depends': ['base','account','purchase_register_new'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_register_new.xml'
    ],
}
