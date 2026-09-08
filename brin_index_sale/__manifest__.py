# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Sales',
    'version': '18.0.1.0.1',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for sales tables via sql.create_index',
    'description': """
BRIN Indexes for Sales (Odoo 18)
================================

Creates BRIN indexes in init() via sql.create_index on:
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
