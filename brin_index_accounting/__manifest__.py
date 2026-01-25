# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Accounting',
    'version': '18.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for accounting tables',
    'description': """
BRIN Indexes for Accounting
===========================

Creates BRIN indexes on:
- account_move_line (date, create_date)
- account_move (date, invoice_date)
- account_partial_reconcile (create_date)
- account_bank_statement_line (date)
- account_payment (date)

These indexes significantly improve performance for date-range queries
on large accounting databases.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['account'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
