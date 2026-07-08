# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Manufacturing using Odoo 19 models.Index (BRIN).
"""
from odoo import models


class MrpProduction(models.Model):
    """BRIN indexes for mrp_production."""
    _inherit = 'mrp.production'

    _brin_date_start = models.Index("USING brin (date_start)")
    _brin_date_finished = models.Index("USING brin (date_finished)")
    _brin_create_date = models.Index("USING brin (create_date)")


class MrpWorkorder(models.Model):
    """BRIN indexes for mrp_workorder."""
    _inherit = 'mrp.workorder'

    _brin_date_start = models.Index("USING brin (date_start)")
    _brin_date_finished = models.Index("USING brin (date_finished)")


class MrpWorkcenterProductivity(models.Model):
    """BRIN indexes for mrp_workcenter_productivity - essential for OEE."""
    _inherit = 'mrp.workcenter.productivity'

    _brin_date_start = models.Index("USING brin (date_start)")
    _brin_date_end = models.Index("USING brin (date_end)")
