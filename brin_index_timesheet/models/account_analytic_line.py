# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Timesheet using Odoo 19 models.Index (BRIN).
"""
from odoo import models


class AccountAnalyticLine(models.Model):
    """BRIN index for account_analytic_line (timesheets)."""
    _inherit = 'account.analytic.line'

    _brin_date = models.Index("USING brin (date)")
