# -*- coding: utf-8 -*-
"""
BRIN Index definitions for HR Work Entry using Odoo 18 _sql_indexes.
"""
from odoo import models


class HrWorkEntry(models.Model):
    """BRIN indexes for hr_work_entry."""
    _inherit = 'hr.work.entry'

    _sql_indexes = [
        models.Index('date_start', type='brin'),
        models.Index('date_stop', type='brin'),
    ]
