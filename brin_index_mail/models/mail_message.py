# -*- coding: utf-8 -*-
"""
BRIN Index definitions for Mail using Odoo 19 models.Index (BRIN).

mail_message is often the largest table in Odoo databases!
"""
from odoo import models


class MailMessage(models.Model):
    """BRIN indexes for mail_message - often the LARGEST table in Odoo!"""
    _inherit = 'mail.message'

    _brin_date = models.Index("USING brin (date)")
    _brin_create_date = models.Index("USING brin (create_date)")


class MailTrackingValue(models.Model):
    """BRIN index for mail_tracking_value - grows fast with tracked fields."""
    _inherit = 'mail.tracking.value'

    _brin_create_date = models.Index("USING brin (create_date)")


# NOTE: mail.notification has no create_date column in Odoo 19 (lightweight
# model — only read_date); no BRIN class for it here.


class BusBus(models.Model):
    """BRIN index for bus_bus - high write volume."""
    _inherit = 'bus.bus'

    _brin_create_date = models.Index("USING brin (create_date)")


class IrAttachment(models.Model):
    """BRIN index for ir_attachment."""
    _inherit = 'ir.attachment'

    _brin_create_date = models.Index("USING brin (create_date)")
