# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - CRM',
    'version': '18.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for CRM tables using Odoo 18 _sql_indexes',
    'description': """
BRIN Indexes for CRM (Odoo 18)
==============================

Uses the new Odoo 18 _sql_indexes mechanism to create BRIN indexes on:
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
