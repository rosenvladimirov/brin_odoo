# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Accounting using Odoo 18 _sql_indexes.

The _sql_indexes attribute uses the new Index() class introduced in Odoo 17+
which supports different index types including BRIN.

Syntax: models.Index(expression, ..., type='brin')
"""
from odoo import models


class AccountMoveLine(models.Model):
    """BRIN indexes for account_move_line - typically the largest table."""
    _inherit = 'account.move.line'

    _sql_indexes = [
        # CRITICAL: date column has excellent correlation (>0.95)
        models.Index('date', type='brin'),
        models.Index('create_date', type='brin'),
    ]


class AccountMove(models.Model):
    """BRIN indexes for account_move (invoices, journal entries)."""
    _inherit = 'account.move'

    _sql_indexes = [
        models.Index('date', type='brin'),
        models.Index('invoice_date', type='brin'),
        models.Index('create_date', type='brin'),
    ]


class AccountPartialReconcile(models.Model):
    """BRIN index for reconciliation records."""
    _inherit = 'account.partial.reconcile'

    _sql_indexes = [
        models.Index('create_date', type='brin'),
    ]


class AccountBankStatementLine(models.Model):
    """BRIN index for bank statement lines."""
    _inherit = 'account.bank.statement.line'

    _sql_indexes = [
        models.Index('date', type='brin'),
    ]


class AccountPayment(models.Model):
    """BRIN index for payments."""
    _inherit = 'account.payment'

    _sql_indexes = [
        models.Index('date', type='brin'),
    ]
