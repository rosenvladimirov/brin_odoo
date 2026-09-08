# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Stock',
    'version': '18.0.1.0.1',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for inventory tables via sql.create_index',
    'description': """
BRIN Indexes for Stock/Inventory (Odoo 18)
==========================================

Creates BRIN indexes in init() via sql.create_index on:
- stock_move_line (date, create_date)
- stock_move (date)
- stock_quant (in_date) - Critical for FIFO/FEFO
- stock_lot (create_date, expiration_date)
- stock_picking (scheduled_date, date_done)
- stock_valuation_layer (create_date)
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    # stock_account носи stock.valuation.layer, който модулът индексира —
    # без тази зависимост _inherit пада с "Model does not exist in registry".
    'depends': ['stock', 'stock_account'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
