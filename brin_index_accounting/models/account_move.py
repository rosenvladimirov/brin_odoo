# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Accounting using Odoo 19 models.Index (BRIN).

Odoo 19 declares indexes as class attributes: _name = models.Index("USING brin (col)").

"""
from odoo import models


class AccountMoveLine(models.Model):
    """BRIN indexes for account_move_line - typically the largest table."""
    _inherit = 'account.move.line'

    _brin_date = models.Index("USING brin (date)")
    _brin_create_date = models.Index("USING brin (create_date)")


class AccountMove(models.Model):
    """BRIN indexes for account_move (invoices, journal entries)."""
    _inherit = 'account.move'

    _brin_date = models.Index("USING brin (date)")
    _brin_invoice_date = models.Index("USING brin (invoice_date)")
    _brin_create_date = models.Index("USING brin (create_date)")


class AccountPartialReconcile(models.Model):
    """BRIN index for reconciliation records."""
    _inherit = 'account.partial.reconcile'

    _brin_create_date = models.Index("USING brin (create_date)")


# NOTE: account.bank.statement.line has no own `date` column in Odoo 19 — the
# accounting date lives on the related account_move (already BRIN-indexed), so
# no separate BRIN class here.


class AccountPayment(models.Model):
    """BRIN index for payments."""
    _inherit = 'account.payment'

    _brin_date = models.Index("USING brin (date)")
