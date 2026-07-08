# -*- coding: utf-8 -*-
"""
BRIN Index definitions for HR Work Entry using Odoo 18 _sql_indexes.
"""
from odoo import models


class HrWorkEntry(models.Model):
    """BRIN indexes for hr_work_entry."""
    _inherit = 'hr.work.entry'

    # Odoo 19 replaced date_start/date_stop with a single NOT NULL `date`.
    _sql_indexes = [
        models.Index('date', type='brin'),
    ]
