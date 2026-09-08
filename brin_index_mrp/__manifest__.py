# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Manufacturing',
    'version': '18.0.1.0.1',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for manufacturing tables via sql.create_index',
    'description': """
BRIN Indexes for Manufacturing (Odoo 18)
========================================

Creates BRIN indexes in init() via sql.create_index on:
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
