{
    'name': 'MAS credit note report Template',
    'version': '14.0.0.2',
    'description': """This module consists, the credit note Templates""",
    'category': 'Localization',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['account','l10n_in','web','base','product','sale',],
    'data': [
        'reports/creditnote_report.xml',
        'views/header_footer.xml',   
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
