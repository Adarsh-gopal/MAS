# -*- coding: utf-8 -*-
{
    'name': 'Asset Base',
    'version': '14.0.5',
    'summary': 'Asset Management',
    'license':'AGPL-3',
    'description': """
     Asset management is to manage assets owned by an organization.
""",
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['base','mail','account_asset'],
    'images': ['static/description/banner.jpg'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/asset_sequence.xml',
        'views/asset_view.xml',
        'views/asset_move_view.xml'
             
             ],
    'installable': True,
    'application': True,
    'auto_install': False,
}


