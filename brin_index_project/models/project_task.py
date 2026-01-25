# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Project using Odoo 18 _sql_indexes.
"""
from odoo import models


class ProjectTask(models.Model):
    """BRIN indexes for project_task."""
    _inherit = 'project.task'

    _sql_indexes = [
        models.Index('date_deadline', type='brin'),
        models.Index('date_end', type='brin'),
        models.Index('create_date', type='brin'),
    ]
