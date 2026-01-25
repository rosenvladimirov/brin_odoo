# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Point of Sale using Odoo 18 _sql_indexes.

POS has HIGH WRITE VOLUME - indexes should be optimized for this.
"""
from odoo import models


class PosOrder(models.Model):
    """BRIN indexes for pos_order - high write volume."""
    _inherit = 'pos.order'

    _sql_indexes = [
        models.Index('date_order', type='brin'),
        models.Index('create_date', type='brin'),
    ]


class PosOrderLine(models.Model):
    """BRIN index for pos_order_line - typically 3-5x more rows than orders."""
    _inherit = 'pos.order.line'

    _sql_indexes = [
        models.Index('create_date', type='brin'),
    ]


class PosPayment(models.Model):
    """BRIN index for pos_payment."""
    _inherit = 'pos.payment'

    _sql_indexes = [
        models.Index('create_date', type='brin'),
    ]


class PosSession(models.Model):
    """BRIN index for pos_session."""
    _inherit = 'pos.session'

    _sql_indexes = [
        models.Index('start_at', type='brin'),
    ]
