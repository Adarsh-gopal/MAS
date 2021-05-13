{
    'name': "Tds Register Report-2",
    'version': '14.0.1',
    'description':'tds report',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'installable': True,
    'application': True,
    'depends': ['base','product','account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/tds_report_history.xml'
        ], 
}


