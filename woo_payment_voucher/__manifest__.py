# -*- coding: utf-8 -*-
{
    "name": "Woo Payment Voucher",
    "version": "14.0.0.2",
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    "summary": """
    """,
    "description": """
        Payment Voucher Print Document
    """,
    "category": "Payment",
    "depends": [
        'account_accountant', 'account', 'base',
    ],
    "data": [
        'views/payment_custom_header.xml',
        'views/payment_reciept.xml',
        'views/supplier_field.xml',
        'data/mail_sub_type.xml',
        
    ],
    "installable": True,
    "auto_install": False,
}
