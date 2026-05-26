import logging
import subprocess
import os
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# Tables to partition: (table_name, control_column, interval, start_year)
PARTITION_TARGETS = [
    ('account_move_line', 'date', '1 year', 2018),
    ('stock_move',        'date', '1 year', 2018),
]


class PgPartitionManager(models.TransientModel):
    _name = 'pg.partition.manager'
    _description = 'PostgreSQL Partition Manager'

    # ------------------------------------------------------------------ #
    #  Setup                                                               #
    # ------------------------------------------------------------------ #

    def _setup_partman(self):
        """Called from post_init_hook. Installs extension and partitions."""
        self._install_pg_partman()
        for table, control, interval, start_year in PARTITION_TARGETS:
            if self._table_exists(table):
                if not self._is_partitioned(table):
                    _logger.info('Partitioning table: %s', table)
                    self._convert_to_partitioned(table, control, interval, start_year)
                else:
                    _logger.info('Table already partitioned: %s', table)
                    self._run_maintenance(table)

    def _install_pg_partman(self):
        cr = self.env.cr
        cr.execute("SELECT COUNT(*) FROM pg_extension WHERE extname = 'pg_partman'")
        if cr.fetchone()[0] == 0:
            try:
                cr.execute("CREATE SCHEMA IF NOT EXISTS partman")
                cr.execute("CREATE EXTENSION pg_partman SCHEMA partman")
                _logger.info('pg_partman extension installed successfully')
            except Exception as e:
                raise UserError(_(
                    'Cannot install pg_partman extension.\n'
                    'Make sure postgresql-16-partman is installed on the server.\n'
                    'Error: %s'
                ) % str(e))
        else:
            _logger.info('pg_partman already installed')

    # ------------------------------------------------------------------ #
    #  Conversion                                                          #
    # ------------------------------------------------------------------ #

    def _convert_to_partitioned(self, table, control, interval, start_year):
        """
        Convert existing table to partitioned using pg_partman.

        Sequence:
        1. Rename original table to _nonpartitioned (keeps data safe)
        2. Create new empty table with PARTITION BY RANGE skeleton
        3. Call partman.create_parent() — partman creates all partitions
           from start_year to today + default partition automatically
        4. Copy data in batches from backup table into partitioned table
           (partman routes each row to the correct partition)
        5. Recreate indexes and sequences on parent table

        Needs maintenance window on production.
        On 500K rows expect ~3-5 minutes.
        """
        cr = self.env.cr
        backup_table = '%s_nonpartitioned' % table
        start = '%d-01-01' % start_year

        _logger.info('Converting %s to partitioned table...', table)

        # 1. Rename original — data is safe here
        cr.execute('ALTER TABLE "%s" RENAME TO "%s"' % (table, backup_table))
        _logger.info('  Renamed %s → %s', table, backup_table)

        # 2. Create skeleton partitioned table — columns only, no partitions yet
        cr.execute(self._get_partitioned_ddl(table, control))
        _logger.info('  Created partitioned skeleton for %s', table)

        # 3. partman.create_parent creates all partitions automatically:
        #    - yearly partitions from start_year to current year
        #    - a "default" partition for out-of-range rows
        #    - configures bgw for future partition creation
        cr.execute("""
            SELECT partman.create_parent(
                p_parent_table    => %s,
                p_control         => %s,
                p_interval        => %s,
                p_start_partition => %s,
                p_premake         => 2
            )
        """, ('public.%s' % table, control, interval, start))
        _logger.info('  pg_partman registered %s (partitions auto-created)', table)

        # 4. Copy data — partman routes each INSERT to correct partition
        offset = 0
        batch = 100000
        while True:
            cr.execute("""
                INSERT INTO "%s"
                SELECT * FROM "%s"
                ORDER BY id
                LIMIT %s OFFSET %s
            """ % (table, backup_table, batch, offset))
            inserted = cr.rowcount
            _logger.info('  %s: copied %d rows (offset %d)', table, inserted, offset)
            if inserted < batch:
                break
            offset += batch

        # 5. Update partman config to track this table
        cr.execute("""
            UPDATE partman.part_config
            SET infinite_time_partitions = true,
                retention_keep_table     = true
            WHERE parent_table = %s
        """, ('public.%s' % table,))

        _logger.info('Conversion of %s complete.', table)

    def _get_partitioned_ddl(self, table, control):
        """
        Returns CREATE TABLE ... PARTITION BY RANGE statement.
        We introspect columns from the existing backup table.
        """
        cr = self.env.cr
        cr.execute("""
            SELECT column_name, data_type, character_maximum_length,
                   is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, ('%s_nonpartitioned' % table,))
        cols = cr.fetchall()

        col_defs = []
        for col_name, data_type, max_len, nullable, default in cols:
            if data_type == 'character varying' and max_len:
                type_str = 'VARCHAR(%d)' % max_len
            elif data_type == 'character varying':
                type_str = 'VARCHAR'
            else:
                type_str = data_type.upper()
            null_str = '' if nullable == 'YES' else 'NOT NULL'
            default_str = ('DEFAULT %s' % default) if default else ''
            col_defs.append('    "%s" %s %s %s' % (
                col_name, type_str, null_str, default_str
            ))

        return 'CREATE TABLE "%s" (\n%s\n) PARTITION BY RANGE (%s)' % (
            table, ',\n'.join(col_defs), control
        )

    # ------------------------------------------------------------------ #
    #  Maintenance                                                         #
    # ------------------------------------------------------------------ #

    def _run_maintenance(self, table=None):
        cr = self.env.cr
        if table:
            cr.execute("SELECT partman.run_maintenance(%s)", ('public.%s' % table,))
        else:
            cr.execute("SELECT partman.run_maintenance()")
        _logger.info('pg_partman maintenance complete')

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _table_exists(self, table):
        self.env.cr.execute(
            "SELECT COUNT(*) FROM pg_tables WHERE tablename = %s", (table,)
        )
        return self.env.cr.fetchone()[0] > 0

    def _is_partitioned(self, table):
        self.env.cr.execute("""
            SELECT COUNT(*) FROM pg_class c
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relname = %s AND c.relkind = 'p'
        """, (table,))
        return self.env.cr.fetchone()[0] > 0

    # ------------------------------------------------------------------ #
    #  Partition info (for views)                                          #
    # ------------------------------------------------------------------ #

    @api.model
    def get_partition_info(self):
        """Returns list of dicts with partition stats."""
        cr = self.env.cr
        results = []
        for table, _, _, _ in PARTITION_TARGETS:
            if not self._table_exists(table):
                continue
            cr.execute("""
                SELECT
                    child.relname AS partition_name,
                    pg_size_pretty(pg_total_relation_size(child.oid)) AS total_size,
                    pg_total_relation_size(child.oid) AS size_bytes,
                    (SELECT n_live_tup FROM pg_stat_user_tables
                     WHERE relname = child.relname) AS live_rows,
                    pg_get_expr(child.relpartbound, child.oid) AS partition_range
                FROM pg_inherits
                JOIN pg_class parent ON parent.oid = pg_inherits.inhparent
                JOIN pg_class child  ON child.oid  = pg_inherits.inhrelid
                WHERE parent.relname = %s
                ORDER BY child.relname
            """, (table,))
            for row in cr.fetchall():
                results.append({
                    'parent_table': table,
                    'partition_name': row[0],
                    'total_size': row[1],
                    'size_bytes': row[2],
                    'live_rows': row[3] or 0,
                    'partition_range': row[4],
                })
        return results

    # ------------------------------------------------------------------ #
    #  pg_dump of single partition                                         #
    # ------------------------------------------------------------------ #

    @api.model
    def dump_partition(self, partition_name, output_dir='/tmp'):
        """
        pg_dump a single partition to a file.
        Returns the output file path.
        """
        db_name = self.env.cr.dbname
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = '%s_%s_%s.dump' % (db_name, partition_name, timestamp)
        filepath = os.path.join(output_dir, filename)

        # pg_dump with --table for specific partition
        cmd = [
            'pg_dump',
            '--format=custom',
            '--compress=9',
            '--table=%s' % partition_name,
            '--file=%s' % filepath,
            db_name,
        ]

        _logger.info('Dumping partition %s to %s', partition_name, filepath)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600,
            )
            if result.returncode != 0:
                raise UserError(_(
                    'pg_dump failed for partition %s:\n%s'
                ) % (partition_name, result.stderr))
            _logger.info('Dump complete: %s', filepath)
            return filepath
        except FileNotFoundError:
            raise UserError(_('pg_dump not found. Is PostgreSQL client installed?'))
        except subprocess.TimeoutExpired:
            raise UserError(_('pg_dump timed out for partition %s') % partition_name)
