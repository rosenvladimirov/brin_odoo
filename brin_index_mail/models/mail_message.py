# -*- coding: utf-8 -*-
import logging
from odoo import models

_logger = logging.getLogger(__name__)


def create_brin_index(cr, table, column, pages_per_range=32):
    """Create BRIN index if it doesn't exist."""
    index_name = f"brin_{table}_{column}"
    cr.execute("""
        SELECT 1 FROM pg_indexes 
        WHERE schemaname = 'public' AND indexname = %s
    """, (index_name,))
    
    if not cr.fetchone():
        _logger.info("Creating BRIN index %s on %s(%s)", index_name, table, column)
        try:
            cr.execute(f"""
                CREATE INDEX {index_name} 
                ON {table} USING brin({column}) 
                WITH (pages_per_range = {pages_per_range})
            """)
            _logger.info("BRIN index %s created successfully", index_name)
        except Exception as e:
            _logger.warning("Failed to create BRIN index %s: %s", index_name, e)


class MailMessage(models.Model):
    _inherit = 'mail.message'

    def init(self):
        super().init()
        # CRITICAL: mail_message is often the largest table in Odoo!
        # Can grow to 10-200M+ rows in production
        create_brin_index(self.env.cr, 'mail_message', 'date', 32)
        create_brin_index(self.env.cr, 'mail_message', 'create_date', 32)


class MailTrackingValue(models.Model):
    _inherit = 'mail.tracking.value'

    def init(self):
        super().init()
        # Grows very fast - every tracked field change creates a record
        create_brin_index(self.env.cr, 'mail_tracking_value', 'create_date', 32)


class MailNotification(models.Model):
    _inherit = 'mail.notification'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'mail_notification', 'create_date', 32)


class BusBus(models.Model):
    _inherit = 'bus.bus'

    def init(self):
        super().init()
        # High write volume, should be cleaned regularly
        create_brin_index(self.env.cr, 'bus_bus', 'create_date', 16)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'ir_attachment', 'create_date', 64)
