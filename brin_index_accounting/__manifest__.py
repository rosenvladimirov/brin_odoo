# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Accounting',
    'version': '18.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for accounting tables using Odoo 18 _sql_indexes',
    'description': """
BRIN Indexes for Accounting (Odoo 18)
=====================================

Uses the new Odoo 18 _sql_indexes mechanism to create BRIN indexes on:
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
