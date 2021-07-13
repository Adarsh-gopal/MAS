# -*- coding: utf-8 -*-
{
    'name': "Update Analytic accounts for journal items",

    'summary': """ Update Analytic accounts for the journal items which 
     no analytic accounts in the invoice lines
        
        """,

    'description': """
        Update Analytic accounts for the journal items which has no 
        analytic accounts in  the invoice lines
    """,

    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',

    
    'category': 'Uncategorized',
    'version': '14.0.0.1',

   
    'depends': ['base','account'],

  
    'data': [
        'security/ir.model.access.csv',
        'views/account_move.xml',
       
    ],
}
