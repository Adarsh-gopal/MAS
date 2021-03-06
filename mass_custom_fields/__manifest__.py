# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mass Furniture Custom fields',
    'version': '14.0.14',
    'category': 'Manufature',
    'summary': 'For all',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'description': """
This module is display the fields .
    """,
    'depends': ['mrp','stock','base','crm','account','sale_base_14','grn_validation','purchase','product','delivery','sale_stock', 'sale_management','mail','web','sale','maintenance','account_asset','fleet','hr_maintenance'],
    'data': [
        'views/mass_bom_fields_view.xml',
        'wizard/journal_item_update.xml',
        'data/requested_by.xml',
        'security/ir.model.access.csv',
        'views/make_name.xml',
    ],
   
    'installable': True,
    'auto_install': False
}
