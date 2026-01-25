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


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def init(self):
        super().init()
        # HIGH WRITE VOLUME: Use larger pages_per_range
        create_brin_index(self.env.cr, 'pos_order', 'date_order', 64)
        create_brin_index(self.env.cr, 'pos_order', 'create_date', 64)


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    def init(self):
        super().init()
        # Typically 3-5x more rows than orders
        create_brin_index(self.env.cr, 'pos_order_line', 'create_date', 64)


class PosPayment(models.Model):
    _inherit = 'pos.payment'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'pos_payment', 'create_date', 64)


class PosSession(models.Model):
    _inherit = 'pos.session'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'pos_session', 'start_at', 128)
