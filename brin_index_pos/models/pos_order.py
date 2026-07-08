# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Point of Sale using Odoo 19 models.Index (BRIN).

POS has HIGH WRITE VOLUME - indexes should be optimized for this.
"""
from odoo import models


class PosOrder(models.Model):
    """BRIN indexes for pos_order - high write volume."""
    _inherit = 'pos.order'

    _brin_date_order = models.Index("USING brin (date_order)")
    _brin_create_date = models.Index("USING brin (create_date)")


class PosOrderLine(models.Model):
    """BRIN index for pos_order_line - typically 3-5x more rows than orders."""
    _inherit = 'pos.order.line'

    _brin_create_date = models.Index("USING brin (create_date)")


class PosPayment(models.Model):
    """BRIN index for pos_payment."""
    _inherit = 'pos.payment'

    _brin_create_date = models.Index("USING brin (create_date)")


class PosSession(models.Model):
    """BRIN index for pos_session."""
    _inherit = 'pos.session'

    _brin_start_at = models.Index("USING brin (start_at)")
