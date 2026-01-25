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


class HrEmployee(models.Model):
    """Use hr.employee as anchor since it always exists with hr module."""
    _inherit = 'hr.employee'

    def init(self):
        super().init()
        # hr_attendance (from hr_attendance module)
        create_brin_index(self.env.cr, 'hr_attendance', 'check_in', 64)
        create_brin_index(self.env.cr, 'hr_attendance', 'check_out', 64)
        
        # hr_leave (from hr_holidays module)
        create_brin_index(self.env.cr, 'hr_leave', 'date_from', 64)
        
        # hr_payslip (from hr_payroll module)
        create_brin_index(self.env.cr, 'hr_payslip', 'date_from', 64)
        create_brin_index(self.env.cr, 'hr_payslip_line', 'create_date', 32)
        
        # hr_work_entry (from hr_work_entry module)
        create_brin_index(self.env.cr, 'hr_work_entry', 'date_start', 32)
