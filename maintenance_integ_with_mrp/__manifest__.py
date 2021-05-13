# -*- coding: utf-8 -*-
{
    'name': "Maintenance Integration With MRP Odoo 14",

    'summary': """
        Maintenance Integration With MRP consist of creating equipment from Assets and tagging the same to the MO.
        Maintenance request should create a Maintenance Order in the Repair module.""",

    'description': """
        Maintenance Integration With MRP consist of creating equipment from Assets and tagging the same to the MO.
        Maintenance request should create a Maintenance Order in the Repair module.
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",

    'category': 'Maintenance',
    'version': '14.0.2',

    'depends': ['mrp','maintenance_base'],

    'data': [
        'security/ir.model.access.csv',
        'views/mrp.xml',
        'views/equipment_mapping.xml',
    ],
}
