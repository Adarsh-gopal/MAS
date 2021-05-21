# -*- coding: utf-8 -*-
{
    'name': 'Cheque Management',
    'version': '14.2.4',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',

    'category': 'Accounting',
    'summary': 'Cheque Management',
    'description': """Cheque Management""",
    'depends': ['account_accountant', 'account_check_printing'],
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
        'wizard/account_move_reversal_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
