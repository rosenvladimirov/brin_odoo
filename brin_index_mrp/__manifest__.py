# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Manufacturing',
    'version': '19.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for manufacturing tables using Odoo 18 _sql_indexes',
    'description': """
BRIN Indexes for Manufacturing (Odoo 18)
========================================

Uses the new Odoo 18 _sql_indexes mechanism to create BRIN indexes on:
- mrp_production (date_start, date_finished)
- mrp_workorder (date_start, date_finished)
- mrp_workcenter_productivity (date_start, date_end)

Essential for production planning and OEE reports.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['mrp'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
