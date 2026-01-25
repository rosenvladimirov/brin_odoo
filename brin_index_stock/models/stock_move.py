# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Stock using Odoo 18 _sql_indexes.
"""
from odoo import models


class StockMoveLine(models.Model):
    """BRIN indexes for stock_move_line - high volume table."""
    _inherit = 'stock.move.line'

    _sql_indexes = [
        models.Index('date', type='brin'),
        models.Index('create_date', type='brin'),
    ]


class StockMove(models.Model):
    """BRIN indexes for stock_move."""
    _inherit = 'stock.move'

    _sql_indexes = [
        models.Index('date', type='brin'),
        models.Index('create_date', type='brin'),
    ]


class StockQuant(models.Model):
    """BRIN index for stock_quant - Critical for FIFO/FEFO costing."""
    _inherit = 'stock.quant'

    _sql_indexes = [
        # Critical for FIFO/FEFO
        models.Index('in_date', type='brin'),
        models.Index('create_date', type='brin'),
    ]


class StockLot(models.Model):
    """BRIN indexes for stock_lot - important for FEFO."""
    _inherit = 'stock.lot'

    _sql_indexes = [
        models.Index('create_date', type='brin'),
        # Critical for FEFO expiration management
        models.Index('expiration_date', type='brin'),
    ]


class StockPicking(models.Model):
    """BRIN indexes for stock_picking."""
    _inherit = 'stock.picking'

    _sql_indexes = [
        models.Index('scheduled_date', type='brin'),
        models.Index('date_done', type='brin'),
    ]


class StockValuationLayer(models.Model):
    """BRIN index for stock_valuation_layer - grows fast with AVCO/FIFO."""
    _inherit = 'stock.valuation.layer'

    _sql_indexes = [
        models.Index('create_date', type='brin'),
    ]
