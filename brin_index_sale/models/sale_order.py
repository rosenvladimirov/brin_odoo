# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Sales using Odoo 18 _sql_indexes.
"""
from odoo import models


class SaleOrder(models.Model):
    """BRIN indexes for sale_order."""
    _inherit = 'sale.order'

    _sql_indexes = [
        models.Index('date_order', type='brin'),
        models.Index('create_date', type='brin'),
    ]


class SaleOrderLine(models.Model):
    """BRIN index for sale_order_line."""
    _inherit = 'sale.order.line'

    _sql_indexes = [
        models.Index('create_date', type='brin'),
    ]
