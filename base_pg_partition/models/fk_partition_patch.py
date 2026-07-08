"""ORM machinery for partitioned tables.

PostgreSQL forbids a UNIQUE/PK on a partitioned table that does not include
the partition key, so a partitioned parent has no unique on `id` alone — and
therefore CANNOT be the target of an `id`-only foreign key. Odoo's ORM, however,
re-creates every stored Many2one's DB foreign key on each module upgrade
(``Registry.check_foreign_keys``). Left unpatched, the first ``-u`` after a table
is partitioned would try ``ADD FOREIGN KEY ... REFERENCES <partitioned>(id)`` and
crash with "no unique constraint matching given keys".

This patch makes the ORM tolerant of partitioned targets: before the foreign-key
reconciliation runs, it drops from the pending set every FK whose *referenced*
table is partitioned. Referential integrity for those relations is kept at the
Odoo ORM level (the Many2one still enforces existence on write); only the
DB-level FK constraint is skipped.

Scope: only FKs pointing AT a partitioned table are skipped. A partitioned
table's own outbound FKs (pointing at ordinary tables) are created normally.
"""
import logging

from odoo.orm.registry import Registry
from odoo.tools import sql as pg_sql

_logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Patch 2: teach the ORM that a partitioned table (relkind 'p') EXISTS.
# odoo.tools.sql.existing_tables filters relkind IN ('r','v','m') — a
# partitioned parent (relkind 'p') is missed, so on the next `-u` Odoo thinks
# the model has no table and tries to CREATE TABLE ... → "already exists" crash.
# Add 'p' so partitioned parents are recognised. table_exists() delegates to
# existing_tables(), so it is fixed too.
# --------------------------------------------------------------------------- #
if not getattr(pg_sql, "_bpp_existing_tables_patch", False):
    def _existing_tables(cr, tablenames):
        cr.execute(pg_sql.SQL("""
            SELECT c.relname
              FROM pg_class c
             WHERE c.relname IN %s
               AND c.relkind IN ('r', 'v', 'm', 'p')
               AND c.relnamespace = current_schema::regnamespace
        """, tuple(tablenames)))
        return [row[0] for row in cr.fetchall()]

    pg_sql.existing_tables = _existing_tables
    pg_sql._bpp_existing_tables_patch = True
    _logger.info("base_pg_partition: patched sql.existing_tables to recognise "
                 "partitioned tables (relkind 'p')")

# --------------------------------------------------------------------------- #
# Patch 3: don't try to DROP NOT NULL on a primary-key column.
# The partition key (e.g. account_move_line.date) is part of the composite PK
# (id, date) and is set NOT NULL. Odoo's field.update_db_notnull sees the field
# is not `required` and calls sql.drop_not_null → PG raises "column is in a
# primary key". A PK column can never be nullable anyway, so skipping the drop
# is correct (and only affects PK columns).
# --------------------------------------------------------------------------- #
if not getattr(pg_sql, "_bpp_drop_not_null_patch", False):
    _orig_drop_not_null = pg_sql.drop_not_null

    def _drop_not_null(cr, tablename, columnname):
        cr.execute("""
            SELECT 1
              FROM pg_index i
              JOIN pg_attribute a
                ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
             WHERE i.indrelid = %s::regclass
               AND i.indisprimary
               AND a.attname = %s
        """, (tablename, columnname))
        if cr.fetchone():
            _logger.debug(
                "base_pg_partition: skip DROP NOT NULL on PK column %s.%s",
                tablename, columnname)
            return
        return _orig_drop_not_null(cr, tablename, columnname)

    pg_sql.drop_not_null = _drop_not_null
    pg_sql._bpp_drop_not_null_patch = True

_PARTITIONED_SQL = """
    SELECT c.relname
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relkind = 'p' AND n.nspname = current_schema::name
"""

if not getattr(Registry, "_bpp_fk_patch", False):
    _orig_check_foreign_keys = Registry.check_foreign_keys

    def check_foreign_keys(self, cr):
        """Skip pending foreign keys that target a partitioned table."""
        if self._foreign_keys:
            try:
                cr.execute(_PARTITIONED_SQL)
                partitioned = {row[0] for row in cr.fetchall()}
            except Exception:  # noqa: BLE001 — never block init on the probe
                partitioned = set()
            if partitioned:
                # val = (table2, column2, ondelete, model, module); table2 = target
                skipped = [
                    key for key, val in self._foreign_keys.items()
                    if val[0] in partitioned
                ]
                for key in skipped:
                    del self._foreign_keys[key]
                if skipped:
                    _logger.info(
                        "base_pg_partition: skipped %d DB foreign key(s) whose "
                        "target is a partitioned table (ORM keeps app-level RI): %s",
                        len(skipped), sorted(k[0] for k in skipped),
                    )
        return _orig_check_foreign_keys(self, cr)

    Registry.check_foreign_keys = check_foreign_keys
    Registry._bpp_fk_patch = True
    _logger.info("base_pg_partition: installed partitioned-table FK tolerance patch")
