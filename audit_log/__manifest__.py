{
    "name": "Audit Trail",
    "version": "14.0.1.0",
    "sequence": 100,
    "category": "Tools",
    "author": "Prixgen Tech Solutions Pvt. Ltd.",
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    "license": 'LGPL-3',
    "description": """
This module lets administrator track every user operation on
all the objects of the system
(for the moment, only create, write and unlink methods).
    """,
    "depends": [
        'base',
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/audit_rule_view.xml',
        'views/audit_log_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
