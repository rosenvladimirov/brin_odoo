# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Project using Odoo 19 models.Index (BRIN).
"""
from odoo import models


class ProjectTask(models.Model):
    """BRIN indexes for project_task."""
    _inherit = 'project.task'

    _brin_date_deadline = models.Index("USING brin (date_deadline)")
    _brin_date_end = models.Index("USING brin (date_end)")
    _brin_create_date = models.Index("USING brin (create_date)")
