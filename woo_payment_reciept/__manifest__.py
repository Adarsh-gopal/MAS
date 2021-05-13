# -*- coding: utf-8 -*-
{
    "name": "woo_payment_reciept",
    "version": "14.0.0.7",
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    "summary": """
    """,
    "description": """
    """,
    "category": "Payment",
    "depends": [
        'account_accountant', 'account', 'base',
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/payment_custom_header.xml',
        'views/payment_reciept.xml',
        'views/paymentfield.xml',
        'data/mail_sub_type.xml',
        # 'views/custom_menu.xml',

        'views/customer_payment_method.xml',
        # 'views/menus.xml',
    ],
    "installable": True,
    "auto_install": False,
}
