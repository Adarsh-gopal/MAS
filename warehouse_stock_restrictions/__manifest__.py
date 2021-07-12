# -*- coding: utf-8 -*-

{
    'name': "Warehouse Restrictions",

    'summary': """
         Warehouse and Stock Location Restriction on Users.""",

    'description': """
        This Module Restricts the User from Accessing Warehouse and Process Stock Moves other than allowed to Warehouses and Stock Locations.
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",	
    'category': 'Warehouse',
    'version': '14.0.1.4',
    'depends': ['base', 'stock','l10n_in_sale','analytic_account_automatio_warehouse','analytic_account_automation_sales','sale_stock','sale'],

    'data': [

        'users_view.xml',
        'security/security.xml',
        # 'security/ir.model.access.csv',
        'sale_order_view.xml'
    ],
    
    
}
