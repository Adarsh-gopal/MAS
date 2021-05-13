# -*- coding: utf-8 -*-

{
    'name' : "Merge Picking",
    'version' : "14.0.2",
    'author' : "Prixgen Tech Solutions Pvt. Ltd.",
    'company' : "Prixgen Tech Solutions Pvt. Ltd.",
    'description' : """This app will merge one or more Po's to gether for doing GRN""",
    'description' : """Same Vendor is required fro doing merge of GRN""",
    'category' : "Inventory",
    "website" : "https://www.prixgen.com",
    'summary': 'Merge Picking',
    'data': [
             'security/ir.model.access.csv',
             'wizard/merge_picking_view.xml',
             ],
    'depends' : ['sale_management','stock', 'product','sale_stock','purchase'],
    'installable': True,
    'auto_install': False,
}
