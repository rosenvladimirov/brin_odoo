# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Point of Sale',
    'version': '18.0.1.0.1',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for POS tables via sql.create_index',
    'description': """
BRIN Indexes for Point of Sale (Odoo 18)
========================================

Creates BRIN indexes in init() via sql.create_index on:
- pos_order (date_order)
- pos_order_line (create_date)
- pos_payment (create_date)
- pos_session (start_at)

Essential for daily sales reports and Z-reports.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
