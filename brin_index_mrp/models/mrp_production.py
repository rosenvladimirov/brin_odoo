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


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'mrp_production', 'date_start', 64)
        create_brin_index(self.env.cr, 'mrp_production', 'date_finished', 64)
        create_brin_index(self.env.cr, 'mrp_production', 'create_date', 64)


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def init(self):
        super().init()
        create_brin_index(self.env.cr, 'mrp_workorder', 'date_start', 64)
        create_brin_index(self.env.cr, 'mrp_workorder', 'date_finished', 64)


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    def init(self):
        super().init()
        # Essential for OEE calculations
        create_brin_index(self.env.cr, 'mrp_workcenter_productivity', 'date_start', 32)
        create_brin_index(self.env.cr, 'mrp_workcenter_productivity', 'date_end', 32)
