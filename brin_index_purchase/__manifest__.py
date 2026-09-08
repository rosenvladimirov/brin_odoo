# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Purchase',
    'version': '18.0.1.0.1',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for purchasing tables via sql.create_index',
    'description': """
BRIN Indexes for Purchasing (Odoo 18)
=====================================

Creates BRIN indexes in init() via sql.create_index on:
- purchase_order (date_order, date_approve)
- purchase_order_line (date_planned, create_date)

Essential for purchasing analysis and supplier reports.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['purchase'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
