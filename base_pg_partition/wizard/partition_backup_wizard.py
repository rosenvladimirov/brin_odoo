import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PartitionBackupWizard(models.TransientModel):
    _name = 'partition.backup.wizard'
    _description = 'Backup a PostgreSQL Partition'

    partition_name = fields.Char(
        string='Partition',
        required=True,
    )
    parent_table = fields.Char(
        string='Parent Table',
        readonly=True,
    )
    partition_range = fields.Char(
        string='Range',
        readonly=True,
    )
    live_rows = fields.Integer(
        string='Rows',
        readonly=True,
    )
    total_size = fields.Char(
        string='Size',
        readonly=True,
    )
    output_dir = fields.Char(
        string='Output Directory',
        default='/tmp',
        required=True,
    )
    result_path = fields.Char(
        string='Dump File',
        readonly=True,
    )
    state = fields.Selection([
        ('draft', 'Ready'),
        ('done', 'Done'),
    ], default='draft')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Pre-populate partition list for selection
        return res

    def action_dump(self):
        self.ensure_one()
        manager = self.env['pg.partition.manager']
        path = manager.dump_partition(
            self.partition_name,
            output_dir=self.output_dir,
        )
        self.write({
            'result_path': path,
            'state': 'done',
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_run_maintenance(self):
        """Trigger pg_partman maintenance — creates next year partition."""
        manager = self.env['pg.partition.manager']
        manager._run_maintenance()
        return {'type': 'ir.actions.act_window_close'}
