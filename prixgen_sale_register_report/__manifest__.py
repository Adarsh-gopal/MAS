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

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sales_report.xml',
        'wizard/Sale_report_wizard.xml',
        'views/sales_report_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
