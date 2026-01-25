# -*- coding: utf-8 -*-
"""
BRIN Index definitions for HR Holidays using Odoo 18 _sql_indexes.
"""
from odoo import models


class HrLeave(models.Model):
    """BRIN indexes for hr_leave."""
    _inherit = 'hr.leave'

    _sql_indexes = [
        models.Index('date_from', type='brin'),
        models.Index('date_to', type='brin'),
    ]
