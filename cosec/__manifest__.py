# -*- coding: utf-8 -*-
{
    'name': "cosec",

    'summary': """
        Attendence of the employees from biometric device""",

    'description': """
        Attendence details of the employees from cosec device.
        Details of monthly data.
        Leave management.
        Integration of detaiis from cosec device to payroll.

    """,

    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'category': 'Attendence',
    'version': '14.0.10',
    'depends': ['base','hr_attendance','hr','hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/cosec_data.xml',
        'views/employee.xml',
        'views/settings.xml',
        'views/cosec_month.xml',
        'views/leave_management.xml',
        'views/hr_payslip.xml',

    ],
}
