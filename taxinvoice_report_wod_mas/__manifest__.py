{
    'name': 'MAS invoice report Template',
    'version': '14.0.0.17',
    'description': """This module consists, the sale Invoice Templates""",
    'category': 'Localization',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['account','l10n_in','web','base','product','sale',],
    'data': [
        'reports/taxinvoice_report_wd.xml',
        'reports/taxinvoice_report.xml',
        'views/header_footer.xml',   
        'views/copies.xml',   
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
