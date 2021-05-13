{
    'name': "Inventory Backdate",

    'summary': """Total solution for backdate stock & inventory operations""",
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com', 

    'category': 'Warehouse',
    'version': '14.0.1',

    'depends': ['to_stock_picking_backdate'],

    'data': [
        'wizard/stock_inventory_backdate_wizard_views.xml',
        'wizard/stock_scrap_backdate_wizard_views.xml',
        'wizard/stock_warn_insufficient_qty_scrap_views.xml',
    ],

    'images' : [
    	],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'OPL-1',
}
