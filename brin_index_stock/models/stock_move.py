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


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'stock_move_line', 'date', 32)
        create_brin_index(self.env.cr, 'stock_move_line', 'create_date', 32)


class StockMove(models.Model):
    _inherit = 'stock.move'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'stock_move', 'date', 32)
        create_brin_index(self.env.cr, 'stock_move', 'create_date', 64)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def init(self):
        super().init()
        # Critical for FIFO/FEFO costing
        create_brin_index(self.env.cr, 'stock_quant', 'in_date', 64)
        create_brin_index(self.env.cr, 'stock_quant', 'create_date', 64)


class StockLot(models.Model):
    _inherit = 'stock.lot'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'stock_lot', 'create_date', 64)
        # expiration_date is critical for FEFO
        create_brin_index(self.env.cr, 'stock_lot', 'expiration_date', 64)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'stock_picking', 'scheduled_date', 64)
        create_brin_index(self.env.cr, 'stock_picking', 'date_done', 64)


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    def init(self):
        super().init()
        # Critical for inventory valuation reports
        create_brin_index(self.env.cr, 'stock_valuation_layer', 'create_date', 32)
