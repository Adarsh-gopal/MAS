# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Auto Sequance on lead Form',
    'version': '14.0.5',
    'summary': 'This apps helps create/generate automatic sequence of lead',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'description':"""Automatic Sequance on Lead, Lead Sequance, Auto numbering on lead ,Automatic Sequance on oppertunity, oppertunity Sequance, Auto numbering on oppertunity, Automatic Sequance on pipeline, pipeline Sequance, Auto numbering on pipline,""", 
    'license':'OPL-1',
    'depends':['base','sale','crm','sale_crm','sale_management' ],
    'data':[
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/bi_lead.xml',
        'views/res_partner.xml'
        ],
    'installable': True,
    'auto_install': False,
}

