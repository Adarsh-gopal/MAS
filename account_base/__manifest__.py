# -*- coding: utf-8 -*-
{
    'name': "Account Base Odoo14",

    'summary': """
        Base Customization on Accounting""",

    'description': """
        Included Functionalities -
            1) Roundoff.-------------------------------------------(roundoff.py/xml)
            2) Unrelate Bill Date and Accounting date--------------(disconnect.py)
            3) Currency Inverse and precision----------------------(currency_inverce.py/xml)
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",


    'category': 'Customization',
    'version': '14.0.1.7',

    'depends': ['base','account','stock','purchase','account_reports'],

    'data': [
        'views/assets.xml',
        'views/account_reports_aged_receivable.xml',
        'views/currency_inverse.xml',
        'views/currency_rate_views.xml',
        'views/account_move.xml',
        'views/res_config_settings.xml',
        'views/round_off.xml',
        'views/account_reversal.xml',
    ],
    'auto_install': False,
    'installable': True,
}
