# -*- coding: utf-8 -*-
"""
BRIN Index definitions for HR Payroll using Odoo 18 _sql_indexes.
"""
from odoo import models


class HrPayslip(models.Model):
    """BRIN indexes for hr_payslip."""
    _inherit = 'hr.payslip'

    _sql_indexes = [
        models.Index('date_from', type='brin'),
        models.Index('date_to', type='brin'),
    ]


class HrPayslipLine(models.Model):
    """BRIN index for hr_payslip_line - typically 10-20x more rows than payslips."""
    _inherit = 'hr.payslip.line'

    _sql_indexes = [
        models.Index('create_date', type='brin'),
    ]
