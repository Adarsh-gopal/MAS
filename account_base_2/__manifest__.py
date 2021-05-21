# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Account Base 2(only for MAS)',
    'version': '14.0.1.4',
    'category': 'Accounts',
    'summary': 'For Invoice due date visibility',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'description': """
This module is display the Invoice due date in Invoice .
    """,
    'depends': ['account','l10n_in','web','base','product','sale','account_accountant','account_check_printing'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_custom_header.xml',
        'views/payment_reciept.xml',
        'views/paymentfield.xml',
        'views/customer_payment_method.xml',
        'views/payment_inherit.xml',
    ],
   
    'installable': True,
    'auto_install': False
}
