# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Sales using Odoo 19 models.Index (BRIN).
"""
from odoo import models


class SaleOrder(models.Model):
    """BRIN indexes for sale_order."""
    _inherit = 'sale.order'

    _brin_date_order = models.Index("USING brin (date_order)")
    _brin_create_date = models.Index("USING brin (create_date)")


class SaleOrderLine(models.Model):
    """BRIN index for sale_order_line."""
    _inherit = 'sale.order.line'

    _brin_create_date = models.Index("USING brin (create_date)")
