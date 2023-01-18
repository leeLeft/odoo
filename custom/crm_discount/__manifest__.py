# -*- coding: utf-8 -*-

{
    'name': 'crm_discount',
    'description': 'Manage your personal discount.',
    'author': 'Lee',
    'depends': ['crm'],
    'application': True,
    'version': '1.0.0',
    'license': 'LGPL-3',
    'category': 'Sales/CRM',
    'installable': True,
    'auto_install': True,
    'data': [
        'security/ir.model.access.csv',
        'views/crm_customer_contract_view.xml',
        'views/crm_customer_billing_config_view.xml',
        'views/menu.xml',
    ]
}
