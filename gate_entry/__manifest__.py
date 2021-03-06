# -*- coding: utf-8 -*-
{
    'name': "Gate Entry",

    'summary': """
        Gate Entry without Transfer""",

    'description': """
        The intent of the app is to record the details of the vehicle which has entered/exited the warehouse premises.
        Contains details such as vehicle number, Date, PO/SO/other document details, etc.
        Without doing the Gate entry process, it will not be possible to either do GRN or Delivery operations.
    """,

    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': "https://www.prixgen.com",

    'category': 'Custamization',
    'version': '14.0.2.7',

    'depends': ['base', 'stock', 'purchase', 'sale', 'sale_stock','purchase_stock','fleet','close_po'],

    'data': [
        'data/gate_entry_group_access.xml',
        'security/ir.model.access.csv',
        'views/gate_entry.xml',
        'views/gate_entry_user.xml',
        'views/stock_picking.xml',
        'views/purchase_order.xml',
        'views/header_footer.xml',
        'views/gateentry_in_report.xml',
        'views/gateentry_out_report.xml',
        # 'views/res_config_settings.xml',
    ],

    'images': ['images/icon1.png'],

    'css': ['static/src/css/main.css'],
}
