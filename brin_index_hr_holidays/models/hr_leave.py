# -*- coding: utf-8 -*-
"""
BRIN Index definitions for HR Holidays using Odoo 19 models.Index (BRIN).
"""
from odoo import models


class HrLeave(models.Model):
    """BRIN indexes for hr_leave."""
    _inherit = 'hr.leave'

    _brin_date_from = models.Index("USING brin (date_from)")
    _brin_date_to = models.Index("USING brin (date_to)")
