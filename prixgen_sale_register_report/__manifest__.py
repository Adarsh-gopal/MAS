# -*- coding: utf-8 -*-
{
    'name': "Sale Register Report",

    'summary': """
        """,

    'description': """
        This Module Create new submenu under sales reporting in the name of Sale Register Report.
        Providing form view and wizard for sale register.
    """,

    'author': "Prixgen Team",
    'website': "http://www.prixgen.com",

    'category': 'Sales',
    'version': '14.0.4',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale','inventory_base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/Sale_report_wizard.xml',
        'views/sales_report.xml',
        'views/sales_report_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
