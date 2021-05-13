# -*- coding: utf-8 -*-
{
    'name': "Maintenance Base Odoo 14",

    'summary': """
        Maintenance Base consist of stages equipments also contains the job work stage and sequence for maintenance base """,

    'description': """
        Maintenance Base consist of stages equipments also contains the job work stage and sequence for maintenance base 
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",

    'category': 'Maintenance',
    'version': '14.0.6',

    'depends': ['maintenance'],

    'data': [
        'data/maintenance_seq.xml',
        'security/ir.model.access.csv',
        'views/maintenance.xml',
        'views/sub_categories.xml',
        'reports/jobwork_challan.xml',
    ],
}
