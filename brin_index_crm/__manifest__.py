# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - CRM',
    'version': '18.0.1.0.1',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for CRM tables via sql.create_index',
    'description': """
BRIN Indexes for CRM (Odoo 18)
==============================

Creates BRIN indexes in init() via sql.create_index on:
- crm_lead (create_date, date_deadline, date_closed)

Essential for pipeline analysis and forecasting.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['crm'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
