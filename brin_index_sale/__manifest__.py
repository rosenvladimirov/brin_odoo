# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Sales',
    'version': '19.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for sales tables using Odoo 18 _sql_indexes',
    'description': """
BRIN Indexes for Sales (Odoo 18)
================================

Uses the new Odoo 18 _sql_indexes mechanism to create BRIN indexes on:
- sale_order (date_order, create_date)
- sale_order_line (create_date)

Essential for sales analysis and reporting.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
