# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Accounting',
    'version': '18.0.1.0.1',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for accounting tables via sql.create_index',
    'description': """
BRIN Indexes for Accounting (Odoo 18)
=====================================

Creates BRIN indexes in init() via sql.create_index on:
- account_move_line (date, create_date)
- account_move (date, invoice_date)
- account_partial_reconcile (create_date)
- account_bank_statement_line (date)
- account_payment (date)
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['account'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
