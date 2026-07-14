import logging
import subprocess
import os
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ACTIVE conversion targets — tables converted to pg_partman RANGE partitions
# on module install. Each entry:
#   (table, control_column, interval, start_year, set_not_null)
#
# ACTIVE targets use the DROP-FK strategy (decision Rosen, 2026-07-08): every
# high-value BRIN table is FK-referenced, and native PG partitioning needs the
# partition key in the PK (breaking id-only inbound FKs). Rather than mirror the
# control column into dozens of child tables, we DROP the DB-level inbound FK
# constraints (force_fk) — Odoo keeps app-level RI, and fk_partition_patch stops
# the ORM re-creating them on upgrade. Started with account_move_line (the
# general ledger); tables are empty on mec-19 so conversion is pure DDL.
PARTITION_TARGETS = [
    ('account_move_line', 'date',        '1 year', 2018, True),   # date DB-nullable
    ('stock_move',        'date',        '1 year', 2018, False),  # date NOT NULL
    ('mrp_production',    'date_start',  '1 year', 2018, False),  # date_start NOT NULL
    ('mail_message',      'create_date', '1 year', 2018, True),   # create_date nullable
    ('cfx_placement',     'create_date', '1 year', 2026, True),   # CFX SMT placements; 0 inbound FK; append-only, data from 2026
]

# DEFERRED registry — documented but NOT converted. The authoritative record of
# what WOULD be partitioned and why it is blocked, so rollout/maintenance tools
# know the intent. Range-partitioning any of these first requires either
# (a) adding the control column to the PK AND to every inbound-FK child, or
# (b) explicitly dropping DB-level FK integrity (Odoo ORM keeps app-level RI).
#   (table, control_column, interval, control_nullable, inbound_fk_count, note)
DEFERRED_TARGETS = [
    ('account_move',      'date',           '1 year', False, 34,
     'ledger header; control = accounting date (NOT NULL); 34 inbound FK'),
    ('account_move_line', 'date',           '1 year', True,  20,
     'general ledger; control = accounting date `date`. NOTE: date_maturity '
     'was REJECTED as the key — the O19 core source analysis showed it is '
     'populated ONLY on AR/AP payment_term lines + payment liquidity lines, '
     'and is NULL on product/tax/section/note and every misc journal-entry '
     'line (core itself uses COALESCE(date_maturity, date)). `date` is the '
     'reliable column but is DB-nullable in v19 → needs SET NOT NULL '
     '(backfill from move.date). 20 inbound FK. BRIN covers date + '
     'create_date (+ date_maturity for aging queries; BRIN tolerates NULL).'),
    ('stock_move',        'date',           '1 year', False, 20,
     '20 inbound FK incl. self-ref and l10n_bg_price_diff'),
    ('stock_move_line',   'date',           '1 year', False,  9,
     '9 inbound FK'),
    ('mrp_production',    'date_start',     '1 year', False, 28,
     'date_start is required+defaulted (NOT NULL); 28 inbound FK'),
    ('mrp_workorder',     'production_date','1 year', True,  19,
     'control = production_date (stored compute `date_start or '
     'production_id.date_start`) → ALWAYS populated because the MO date_start '
     'is required+defaulted; DB-nullable (compute-store) so SET NOT NULL '
     'formalizes it WITHOUT data backfill. date_start/date_finished are '
     'unsuitable (NULL until planned/started). 19 inbound FK.'),
    ('mail_message',      'create_date',    '1 year', True,  20,
     'append-heavy; create_date NULLABLE + 20 inbound FK'),
]

# Handled by BRIN only — never range-partition. stock_quant is current-state
# (in_date mutates → cross-partition row churn on UPDATE); stock_lot is master
# data (no NOT NULL date; looked up by id/name, not date range → zero pruning
# benefit). crm_lead / pos_order* are not installed; stock_valuation_layer was
# removed in Odoo 19.
BRIN_ONLY = ['stock_quant', 'stock_lot']


class PgPartitionManager(models.TransientModel):
    _name = 'pg.partition.manager'
    _description = 'PostgreSQL Partition Manager'

    # ------------------------------------------------------------------ #
    #  Setup                                                               #
    # ------------------------------------------------------------------ #

    def _setup_partman(self):
        """Called from post_init_hook. Installs the extension and converts any
        ACTIVE targets. With no active targets the module only makes the
        pg_partman infrastructure available (schema + extension + maintenance
        cron) and logs the deferred registry — partitioning stays deferred."""
        self._install_pg_partman()
        if not PARTITION_TARGETS:
            _logger.info(
                'base_pg_partition: no ACTIVE partition targets — partitioning '
                'is DEFERRED (BRIN indexes handle range pruning). pg_partman '
                'infrastructure is ready. Deferred registry: %s',
                ', '.join(t[0] for t in DEFERRED_TARGETS),
            )
            return
        for table, control, interval, start_year, set_not_null in PARTITION_TARGETS:
            if self._table_exists(table):
                if not self._is_partitioned(table):
                    _logger.info('Partitioning table: %s', table)
                    # ACTIVE targets use the drop-FK strategy (force_fk=True).
                    self._convert_to_partitioned(
                        table, control, interval, start_year,
                        set_not_null, force_fk=True)
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
                    'The pg_partman extension must be present in the PostgreSQL '
                    'server image (e.g. postgresql-17-partman on a Debian base, '
                    'or a custom CloudNativePG operand image that bundles '
                    'pg_partman) and shared_preload_libraries must include '
                    "'pg_partman_bgw'.\nError: %s"
                ) % str(e))
        else:
            _logger.info('pg_partman already installed')

    # ------------------------------------------------------------------ #
    #  Conversion                                                          #
    # ------------------------------------------------------------------ #

    def _inbound_fk_count(self, table):
        """Number of foreign keys in OTHER tables that reference *table*.
        A partitioned table cannot keep these unless the control column is
        folded into its PK and every child references the composite key."""
        self.env.cr.execute(
            "SELECT count(*) FROM pg_constraint "
            "WHERE contype = 'f' AND confrelid = %s::regclass",
            ('public.%s' % table,),
        )
        return self.env.cr.fetchone()[0]

    def _convert_to_partitioned(self, table, control, interval, start_year,
                                set_not_null=False, force_fk=False):
        """
        Convert existing table to partitioned using pg_partman.

        Sequence:
        1. (guard) refuse if inbound FKs exist unless force_fk
        2. (optional) SET NOT NULL on the control column (partition key must be
           NOT NULL; Odoo populates it at ORM level but the DB column may allow
           NULL — e.g. account_move_line.date / mail_message.create_date in v19)
        3. Rename original table to _nonpartitioned (keeps data safe)
        4. Create new empty table with PARTITION BY RANGE skeleton
        5. partman.create_parent() — creates partitions from start_year + default
        6. Copy data in batches (partman routes each row to its partition)
        7. Update partman config

        Needs maintenance window on production. On 500K rows expect ~3-5 minutes.
        """
        cr = self.env.cr

        # 1. SAFETY GUARD — native partitioning needs the control column inside
        #    the PK, which breaks every inbound FK. Do not silently drop referen-
        #    tial integrity: refuse unless the caller has handled the composite-FK
        #    migration and passes force_fk=True.
        inbound = self._inbound_fk_count(table)
        if inbound and not force_fk:
            raise UserError(_(
                'Refusing to partition "%s": it has %d inbound foreign key(s). '
                'Native PostgreSQL range-partitioning requires the partition key '
                '(%s) inside the primary key, which breaks every FK referencing '
                'this table. Perform the composite-FK migration first (add %s to '
                'the PK and to each child FK), or pass force_fk=True to drop '
                'DB-level FK integrity intentionally (Odoo keeps app-level RI).'
            ) % (table, inbound, control, control))

        backup_table = '%s_nonpartitioned' % table
        start = '%d-01-01' % start_year

        _logger.info('Converting %s to partitioned table...', table)

        # 2. Ensure the control column is NOT NULL (partition key requirement).
        if set_not_null:
            # Backfill any NULLs before enforcing NOT NULL. Generic fallback so
            # it works whether the control column is `date` (→ create_date) or
            # `create_date` itself (→ write_date/now); every Odoo table has
            # create_date/write_date.
            cr.execute(
                'UPDATE "%s" SET "%s" = COALESCE(create_date, write_date, now()) '
                'WHERE "%s" IS NULL' % (table, control, control))
            cr.execute(
                'ALTER TABLE "%s" ALTER COLUMN "%s" SET NOT NULL'
                % (table, control))
            _logger.info('  SET NOT NULL on %s.%s', table, control)

        # 2b. force_fk: drop DB-level inbound FK constraints. A partitioned
        #     table cannot be an id-only FK target (no unique on id alone). The
        #     Odoo ORM keeps app-level referential integrity, and
        #     fk_partition_patch stops Odoo re-creating these FKs on upgrade.
        if force_fk and inbound:
            cr.execute("""
                SELECT conrelid::regclass::text, conname
                FROM pg_constraint
                WHERE contype = 'f' AND confrelid = %s::regclass
            """, ('public.%s' % table,))
            for child_table, conname in cr.fetchall():
                cr.execute(
                    'ALTER TABLE %s DROP CONSTRAINT "%s"' % (child_table, conname))
            _logger.info(
                '  dropped %d inbound FK constraint(s) targeting %s', inbound, table)

        # 3. Rename original — data is safe here
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

        # Composite PK (id, control): PostgreSQL requires the partition key in
        # the primary key. `id` keeps its sequence default so it stays globally
        # unique in practice; the ORM addresses rows by id as before.
        col_defs.append('    PRIMARY KEY ("id", "%s")' % control)

        return 'CREATE TABLE "%s" (\n%s\n) PARTITION BY RANGE ("%s")' % (
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
