# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Purchasing using Odoo 18 _sql_indexes.
"""
from odoo import models


class PurchaseOrder(models.Model):
    """BRIN indexes for purchase_order."""
    _inherit = 'purchase.order'

    _sql_indexes = [
        models.Index('date_order', type='brin'),
        models.Index('date_approve', type='brin'),
        models.Index('create_date', type='brin'),
    ]


class PurchaseOrderLine(models.Model):
    """BRIN indexes for purchase_order_line."""
    _inherit = 'purchase.order.line'

    _sql_indexes = [
        models.Index('date_planned', type='brin'),
        models.Index('create_date', type='brin'),
    ]
