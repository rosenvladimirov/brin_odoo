# -*- coding: utf-8 -*-
"""
BRIN Index definitions for HR Attendance using Odoo 18 _sql_indexes.
"""
from odoo import models


class HrAttendance(models.Model):
    """BRIN indexes for hr_attendance."""
    _inherit = 'hr.attendance'

    _sql_indexes = [
        models.Index('check_in', type='brin'),
        models.Index('check_out', type='brin'),
    ]
