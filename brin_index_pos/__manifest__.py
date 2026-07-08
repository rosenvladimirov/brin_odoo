# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Point of Sale',
    'version': '19.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for POS tables using Odoo 18 _sql_indexes',
    'description': """
BRIN Indexes for Point of Sale (Odoo 18)
========================================

Uses the new Odoo 18 _sql_indexes mechanism to create BRIN indexes on:
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
