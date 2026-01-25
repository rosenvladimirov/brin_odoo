# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Stock',
    'version': '18.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for inventory tables',
    'description': """
BRIN Indexes for Stock/Inventory
================================

Creates BRIN indexes on:
- stock_move_line (date, create_date)
- stock_move (date)
- stock_quant (in_date) - Critical for FIFO/FEFO
- stock_lot (create_date, expiration_date)
- stock_picking (scheduled_date, date_done)
- stock_valuation_layer (create_date)

Essential for inventory valuation and traceability queries.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['stock'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
