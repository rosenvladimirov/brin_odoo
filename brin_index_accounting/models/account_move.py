# -*- coding: utf-8 -*-
import logging
from odoo import models

_logger = logging.getLogger(__name__)


def create_brin_index(cr, table, column, pages_per_range=32):
    """Create BRIN index if it doesn't exist."""
    index_name = f"brin_{table}_{column}"
    cr.execute("""
        SELECT 1 FROM pg_indexes 
        WHERE schemaname = 'public' AND indexname = %s
    """, (index_name,))
    
    if not cr.fetchone():
        _logger.info("Creating BRIN index %s on %s(%s)", index_name, table, column)
        try:
            cr.execute(f"""
                CREATE INDEX {index_name} 
                ON {table} USING brin({column}) 
                WITH (pages_per_range = {pages_per_range})
            """)
            _logger.info("BRIN index %s created successfully", index_name)
        except Exception as e:
            _logger.warning("Failed to create BRIN index %s: %s", index_name, e)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def init(self):
        super().init()
        # CRITICAL: account_move_line is usually the largest table
        # date column has excellent correlation (>0.95)
        create_brin_index(self.env.cr, 'account_move_line', 'date', 32)
        create_brin_index(self.env.cr, 'account_move_line', 'create_date', 32)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'account_move', 'date', 64)
        create_brin_index(self.env.cr, 'account_move', 'invoice_date', 64)
        create_brin_index(self.env.cr, 'account_move', 'create_date', 64)


class AccountPartialReconcile(models.Model):
    _inherit = 'account.partial.reconcile'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'account_partial_reconcile', 'create_date', 64)


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'account_bank_statement_line', 'date', 64)


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'account_payment', 'date', 64)
