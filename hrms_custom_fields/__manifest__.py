{
    'name': 'Full And Final custom fields',
    'version': '14.0.2',
    'category': 'Human Resources',
    'author':  'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'summary': 'Required custom fields in employee module for mass',
    'description': "",
    'website': 'https://www.prixgen.com/',
    'depends': [
        'hr',
        'hr_recruitment',
        'hr_skills',
        'base',
        
        'web',
        'hr_payroll',
        'hr_contract','loan',
    ],
    'data': [
    'data/sequencer.xml',
    'data/birthday_wish_cron.xml',
    'data/birthday_wish_template.xml',
    'security/ir.model.access.csv',
    'views/hr_employee_form.xml',
    'views/education.xml',
    'views/res_partner_form_view.xml',
    'views/res_bank.xml',
    'views/hr_recruitment.xml',
    'views/custom_model_views.xml',
    'views/hr_contract.xml',
    'views/hr_payslip.xml',

    ],
    
    'installable': True,
    'application': True,
    'auto_install': False
}
