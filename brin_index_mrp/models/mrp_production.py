# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Manufacturing using Odoo 18 _sql_indexes.
"""
from odoo import models


class MrpProduction(models.Model):
    """BRIN indexes for mrp_production."""
    _inherit = 'mrp.production'

    _sql_indexes = [
        models.Index('date_start', type='brin'),
        models.Index('date_finished', type='brin'),
        models.Index('create_date', type='brin'),
    ]


class MrpWorkorder(models.Model):
    """BRIN indexes for mrp_workorder."""
    _inherit = 'mrp.workorder'

    _sql_indexes = [
        models.Index('date_start', type='brin'),
        models.Index('date_finished', type='brin'),
    ]


class MrpWorkcenterProductivity(models.Model):
    """BRIN indexes for mrp_workcenter_productivity - essential for OEE."""
    _inherit = 'mrp.workcenter.productivity'

    _sql_indexes = [
        # Essential for OEE calculations
        models.Index('date_start', type='brin'),
        models.Index('date_end', type='brin'),
    ]
