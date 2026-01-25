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
        # Check if table exists first
        cr.execute("""
            SELECT 1 FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = %s
        """, (table,))
        if not cr.fetchone():
            _logger.debug("Table %s does not exist, skipping BRIN index", table)
            return
            
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


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'project_task', 'date_deadline', 64)
        create_brin_index(self.env.cr, 'project_task', 'date_end', 64)
        create_brin_index(self.env.cr, 'project_task', 'create_date', 64)
        
        # account_analytic_line for timesheets
        create_brin_index(self.env.cr, 'account_analytic_line', 'date', 32)
