# -*- coding: utf-8 -*-
"""
BRIN Index definitions for HR Work Entry using Odoo 19 models.Index (BRIN).
"""
from odoo import models


class HrWorkEntry(models.Model):
    """BRIN indexes for hr_work_entry."""
    _inherit = 'hr.work.entry'

    # Odoo 19 replaced date_start/date_stop with a single NOT NULL `date`.
    _brin_date = models.Index("USING brin (date)")
