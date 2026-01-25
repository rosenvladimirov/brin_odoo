# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Mail',
    'version': '18.0.1.0.0',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for messaging tables using Odoo 18 _sql_indexes',
    'description': """
BRIN Indexes for Messaging (Odoo 18)
====================================

Uses the new Odoo 18 _sql_indexes mechanism to create BRIN indexes on:
- mail_message (date, create_date) - Often the LARGEST table!
- mail_tracking_value (create_date)
- mail_notification (create_date)
- bus_bus (create_date)
- ir_attachment (create_date)

mail_message is often the silent performance killer in Odoo.
    """,
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['mail'],
    'data': [],
    'auto_install': True,
    'installable': True,
}
