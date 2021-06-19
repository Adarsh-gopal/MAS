# See LICENSE file for full copyright and licensing details.
#Changes Made By Prixgen Tech Solutions Pvt Ltd.
{
    'name': 'Purchase Approval',
    'version': '14.0.4   ',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Purchase Approval',
    'description': " Purchase Approval",
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': "https://www.prixgen.com",

    'depends': ['base','sale',
        'sale_management','purchase_base_14'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/purchase_reject_views.xml',
        'views/purchase_approval_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
