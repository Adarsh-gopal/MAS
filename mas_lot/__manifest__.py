
{
    'name': 'MAS lot	',
    'version': '14.0.1.8',
    'summary': 'Lot no.',
    'description': """
    This module provides features to manage basic quality assurance procedures.
    """,
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
     'website': 'https://www.prixgen.com',
    'category': 'Inventory',
    'depends': ['product','stock','quality'],
    'data': [
        #'data/ktc_lot.xml', 
        'views/lot_seq.xml',     
    ],
    'demo': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': True
}
