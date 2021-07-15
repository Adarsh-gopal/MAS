# -*- coding: utf-8 -*-

{
    'name': 'Create Contract Employee',
    'version': '14.0.1',
    'category': 'Employee',
    
    'summary': 'contract employee details',
    'description': "",
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['base','hr','hr_payroll',
    ],
    'data': [
        'views/hr_employee.xml',      
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}