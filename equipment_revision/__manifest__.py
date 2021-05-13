# -*- coding: utf-8 -*-
{
    'name': "Equipment revision Odoo 14",

    'summary': """
        This module is used to keep the track of equipment revision.""",

    'description': """
      This module is used to keep the track of equipment revision.
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",

    'category': 'Maintenance',
    'version': '14.0.3',

    'depends': ['maintenance','maintenance_base','maintenance_integ_with_asset'],

    'data': [
        'security/ir.model.access.csv',
        'views/maintenance.xml',
    ],
}
