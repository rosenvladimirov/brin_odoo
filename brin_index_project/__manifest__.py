# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Project',
    'version': '18.0.1.0.1',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for project tables via sql.create_index',
    'description': """
BRIN Indexes for Project Management (Odoo 18)
=============================================

Creates BRIN indexes in init() via sql.create_index on:
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
