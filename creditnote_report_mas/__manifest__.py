{
    'name': 'MAS credit note report Template',
    'version': '14.0.0.7',
    'description': """This module consists, the credit note Templates""",
    'category': 'Localization',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['account','l10n_in','web','base','product','sale',],
    'data': [
        'reports/creditnote_report.xml',
        'reports/debitnote.xml',
        'views/header_footer.xml',   
        'views/debitcustomer_report.xml',   
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
