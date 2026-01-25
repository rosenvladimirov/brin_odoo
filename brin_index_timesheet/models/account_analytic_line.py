# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Timesheet using Odoo 18 _sql_indexes.
"""
from odoo import models


class AccountAnalyticLine(models.Model):
    """BRIN index for account_analytic_line (timesheets)."""
    _inherit = 'account.analytic.line'

    _sql_indexes = [
        # Can be very large with timesheets
        models.Index('date', type='brin'),
    ]
