# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - HR Attendance',
    'version': '18.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for attendance tables using Odoo 18 _sql_indexes',
    'description': """
BRIN Indexes for HR Attendance (Odoo 18)
========================================

Uses the new Odoo 18 _sql_indexes mechanism to create BRIN indexes on:
- hr_attendance (check_in, check_out)

Essential for attendance reports and overtime calculations.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['hr_attendance'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
