# -*- coding: utf-8 -*-
{
    'name': 'BRIN Index - Mail',
    'version': '18.0.1.0.1',
    'category': 'Technical/Database',
    'summary': 'BRIN indexes for messaging tables via sql.create_index',
    'description': """
BRIN Indexes for Messaging (Odoo 18)
====================================

Creates BRIN indexes in init() via sql.create_index on:
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
