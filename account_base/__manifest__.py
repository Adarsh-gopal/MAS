# -*- coding: utf-8 -*-
{
    'name': "Account Base Odoo14",

    'summary': """
        Base Customization on Accounting""",

    'description': """
        Included Functionalities -
            1)   Round Off automation
            2)   Currency Inverse Precision
            3)   Unrelated Bill Date and Accounting date only in case of Vendor Bills
            4)   Accounting date not less than Bill date
            5)   Negative filter in Aged payable and receivable
            6)   Analytical Account group filter
            7)   Custom Invoice Sequence
            8)   Custom credit not and debit note sequence
            9)  Bank/cash payment sequence
            10)  Bank/cash receipt sequence
            11)  Item group,PG1,PG2,PG3 in invoice report
            12)  Journal wise Ceiling limit
            13)  Payment Type in Journal entry
            14)  Due date in Vendor bill tree view
    """,

    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",


    'category': 'Customization',
    'version': '14.0.2.1',

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
