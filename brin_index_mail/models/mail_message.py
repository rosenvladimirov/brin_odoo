# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Mail using Odoo 18 _sql_indexes.

mail_message is often the largest table in Odoo databases!
"""
from odoo import models


class MailMessage(models.Model):
    """BRIN indexes for mail_message - often the LARGEST table in Odoo!"""
    _inherit = 'mail.message'

    _sql_indexes = [
        # CRITICAL: Can grow to 10-200M+ rows in production
        models.Index('date', type='brin'),
        models.Index('create_date', type='brin'),
    ]


class MailTrackingValue(models.Model):
    """BRIN index for mail_tracking_value - grows fast with tracked fields."""
    _inherit = 'mail.tracking.value'

    _sql_indexes = [
        # Every tracked field change creates a record here
        models.Index('create_date', type='brin'),
    ]


class MailNotification(models.Model):
    """BRIN index for mail_notification."""
    _inherit = 'mail.notification'

    _sql_indexes = [
        models.Index('create_date', type='brin'),
    ]


class BusBus(models.Model):
    """BRIN index for bus_bus - high write volume."""
    _inherit = 'bus.bus'

    _sql_indexes = [
        # High write volume, should be cleaned regularly
        models.Index('create_date', type='brin'),
    ]


class IrAttachment(models.Model):
    """BRIN index for ir_attachment."""
    _inherit = 'ir.attachment'

    _sql_indexes = [
        models.Index('create_date', type='brin'),
    ]
