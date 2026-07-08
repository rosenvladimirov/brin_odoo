# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Stock using Odoo 19 models.Index (BRIN).
"""
from odoo import models


class StockMoveLine(models.Model):
    """BRIN indexes for stock_move_line - high volume table."""
    _inherit = 'stock.move.line'

    _brin_date = models.Index("USING brin (date)")
    _brin_create_date = models.Index("USING brin (create_date)")


class StockMove(models.Model):
    """BRIN indexes for stock_move."""
    _inherit = 'stock.move'

    _brin_date = models.Index("USING brin (date)")
    _brin_create_date = models.Index("USING brin (create_date)")


class StockQuant(models.Model):
    """BRIN index for stock_quant - Critical for FIFO/FEFO costing."""
    _inherit = 'stock.quant'

    _brin_in_date = models.Index("USING brin (in_date)")
    _brin_create_date = models.Index("USING brin (create_date)")


class StockLot(models.Model):
    """BRIN indexes for stock_lot - important for FEFO."""
    _inherit = 'stock.lot'

    _brin_create_date = models.Index("USING brin (create_date)")
    _brin_expiration_date = models.Index("USING brin (expiration_date)")


class StockPicking(models.Model):
    """BRIN indexes for stock_picking."""
    _inherit = 'stock.picking'

    _brin_scheduled_date = models.Index("USING brin (scheduled_date)")
    _brin_date_done = models.Index("USING brin (date_done)")


# NOTE: stock.valuation.layer was REMOVED in Odoo 19 (valuation refactored) —
# the model no longer exists, so no BRIN class for it here.
