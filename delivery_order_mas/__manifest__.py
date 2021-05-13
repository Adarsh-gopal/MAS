{
    'name': 'Sale Order report Template',
    'version': '14.0.0.8',
    'description': """This module consists, the sale order Templates""",
    'category': 'Localization',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['sale','l10n_in','web','base',],
    'data': [
        'reports/deliveryorder_report.xml',
        'views/header_footer.xml',   
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
