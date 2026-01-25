# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Sales',
    'version': '18.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for sales tables',
    'description': """
BRIN Indexes for Sales
======================

Creates BRIN indexes on:
- sale_order (date_order, create_date)
- sale_order_line (create_date)
- crm_lead (create_date, date_deadline, date_closed)

Essential for sales analysis and pipeline reports.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
