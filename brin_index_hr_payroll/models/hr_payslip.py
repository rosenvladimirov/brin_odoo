# -*- coding: utf-8 -*-
"""
BRIN Index definitions for HR Payroll using Odoo 19 models.Index (BRIN).
"""
from odoo import models


class HrPayslip(models.Model):
    """BRIN indexes for hr_payslip."""
    _inherit = 'hr.payslip'

    _brin_date_from = models.Index("USING brin (date_from)")
    _brin_date_to = models.Index("USING brin (date_to)")


class HrPayslipLine(models.Model):
    """BRIN index for hr_payslip_line - typically 10-20x more rows than payslips."""
    _inherit = 'hr.payslip.line'

    _brin_create_date = models.Index("USING brin (create_date)")
