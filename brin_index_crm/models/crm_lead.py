# -*- coding: utf-8 -*-
"""
BRIN Index definitions for CRM using Odoo 19 models.Index (BRIN).
"""
from odoo import models


class CrmLead(models.Model):
    """BRIN indexes for crm_lead."""
    _inherit = 'crm.lead'

    _brin_create_date = models.Index("USING brin (create_date)")
    _brin_date_deadline = models.Index("USING brin (date_deadline)")
    _brin_date_closed = models.Index("USING brin (date_closed)")
