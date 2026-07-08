# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Project',
    'version': '19.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for project tables using Odoo 18 _sql_indexes',
    'description': """
BRIN Indexes for Project Management (Odoo 18)
=============================================

Uses the new Odoo 18 _sql_indexes mechanism to create BRIN indexes on:
- project_task (date_deadline, date_end, create_date)

Essential for task tracking and project reporting.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['project'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
