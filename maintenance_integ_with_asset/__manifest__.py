# -*- coding: utf-8 -*-
{
    'name': "Maintenance Integration With Asset ",

    'summary': """
        Maintenance Integration With  Asset""",

    'description': """
        Maintenance Integration With  Aasset.
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",

    'category': 'Maintenance',
    'version': '14.0.4',

    'depends': ['account_asset','maintenance','maintenance_base'],

    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/account_assets.xml',
        'views/maintenance_equipment.xml',
        'wizards/genrate_equipment_wiz.xml',
    ],
    'qweb': [
        "static/src/xml/extended_kanabn_button.xml",
        ],
}
