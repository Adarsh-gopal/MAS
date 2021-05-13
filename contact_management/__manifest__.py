# -*- coding: utf-8 -*-

{
    'name': 'Create Customer From Lead',
    'version': '14.0.1.2',
    'category': 'CRM',
    
    'summary': '',
    'description': "",
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': [
        'crm',
        'base',
        'sale',
        'partner_category',
        'purchase',
    ],
    'data': [
        'security/contact_approval.xml',      
        'security/ir.model.access.csv',      
        'wizards/reject_reason.xml',       
        'views/res_partner.xml',      
        'views/sale_order.xml',      
    ],
    # 'qweb': [
    #     "static/src/xml/formselection.xml",
    #     ],
    'installable': True,
    'application': True,
    'auto_install': False
}