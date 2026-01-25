# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Project',
    'version': '18.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for project management tables',
    'description': """
BRIN Indexes for Project Management
===================================

Creates BRIN indexes on:
- project_task (date_deadline, date_end, create_date)
- account_analytic_line (date) - if timesheet is installed

Essential for task tracking and project reporting.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['project'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
