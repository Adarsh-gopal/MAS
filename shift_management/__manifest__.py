# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
{
    'name': 'shift management',
    'version': '14.0.3',
    'summary': 'This apps helps management the people based on the shifts',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'description':"""shift management""", 

    'depends':['base','mrp','hr' ,'manufacturing_base','hr_holidays','resource'],
    'data':[

        'security/ir.model.access.csv',
        'views/mrp_routing_workcenter_shift_view.xml',
        ],
    'installable': True,
    'auto_install': False,
}

