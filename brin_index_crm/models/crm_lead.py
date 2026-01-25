# -*- coding: utf-8 -*-
"""
BRIN Index definitions for CRM using Odoo 18 _sql_indexes.
"""
from odoo import models


class CrmLead(models.Model):
    """BRIN indexes for crm_lead."""
    _inherit = 'crm.lead'

    _sql_indexes = [
        models.Index('create_date', type='brin'),
        models.Index('date_deadline', type='brin'),
        models.Index('date_closed', type='brin'),
    ]
