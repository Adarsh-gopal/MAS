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
    'version': '14.0.1.5.1',

    'depends': ['base','account','stock','purchase'],

    'data': [
        # 'security/ir.model.access.csv',
        # 'security/account_cost_center_security.xml',
        # 'data/account_financial_report_data.xml',
        # 'views/account_invoice_report.xml',
        # 'views/account_cost_center.xml',
        # 'views/account_move_line.xml',
        # 'views/report_financial.xml',
        'views/currency_inverse.xml',
        'views/currency_rate_views.xml',
        'views/account_move.xml',
        # 'views/account_account.xml',
        # 'views/account_invoice.xml',
        'views/res_config_settings.xml',
        'views/round_off.xml',
        'views/account_reversal.xml',
    ],
    'auto_install': True,
    'installable': True,
}
