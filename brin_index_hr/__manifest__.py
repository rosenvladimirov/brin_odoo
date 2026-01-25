# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Human Resources',
    'version': '18.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for HR tables',
    'description': """
BRIN Indexes for Human Resources
================================

Creates BRIN indexes on:
- hr_attendance (check_in, check_out)
- hr_leave (date_from)
- hr_payslip (date_from)
- hr_payslip_line (create_date)
- hr_work_entry (date_start)

Essential for attendance reports and payroll processing.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['hr'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
