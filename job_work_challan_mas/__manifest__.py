{
    'name': 'Job Work Challan report Template',
    'version': '14.0.0.1',
    'description': """This module consists, the Job Work Challan Templates""",
    'category': 'Localization',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['purchase','l10n_in','web','base',],
    'data': [
        'reports/jobwork_challan_report.xml',
        'views/header_footer.xml',   
        'reports/maintenance_request_extra.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
