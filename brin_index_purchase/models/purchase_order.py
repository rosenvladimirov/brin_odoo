# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Purchasing using Odoo 19 models.Index (BRIN).
"""
from odoo import models


class PurchaseOrder(models.Model):
    """BRIN indexes for purchase_order."""
    _inherit = 'purchase.order'

    _brin_date_order = models.Index("USING brin (date_order)")
    _brin_date_approve = models.Index("USING brin (date_approve)")
    _brin_create_date = models.Index("USING brin (create_date)")


class PurchaseOrderLine(models.Model):
    """BRIN indexes for purchase_order_line."""
    _inherit = 'purchase.order.line'

    _brin_date_planned = models.Index("USING brin (date_planned)")
    _brin_create_date = models.Index("USING brin (create_date)")
