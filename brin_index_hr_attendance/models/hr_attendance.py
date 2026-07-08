# -*- coding: utf-8 -*-
"""
BRIN Index definitions for HR Attendance using Odoo 19 models.Index (BRIN).
"""
from odoo import models


class HrAttendance(models.Model):
    """BRIN indexes for hr_attendance."""
    _inherit = 'hr.attendance'

    _brin_check_in = models.Index("USING brin (check_in)")
    _brin_check_out = models.Index("USING brin (check_out)")
