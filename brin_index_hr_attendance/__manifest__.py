# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - HR Attendance',
    'version': '18.0.1.0.1',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for attendance tables via sql.create_index',
    'description': """
BRIN Indexes for HR Attendance (Odoo 18)
========================================

Creates BRIN indexes in init() via sql.create_index on:
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
