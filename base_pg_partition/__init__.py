from . import models
from . import wizard


def post_load():
    """Server-wide hook — installs the partitioned-table ORM tolerance patch
    (sql.existing_tables + registry.check_foreign_keys) BEFORE the module graph
    loads, so account._auto_init sees a partitioned account_move_line as an
    existing table and does not try to re-CREATE it.

    Requires this module in ``server_wide_modules`` (odoo.conf) / ``--load``.
    Importing models already applies the patch at import time; this is the
    explicit, documented entry point Odoo calls in the server-wide phase."""
    from .models import fk_partition_patch  # noqa: F401 — applies the monkeypatch


def post_init_hook(env):
    """Install pg_partman and partition accounting tables."""
    env['pg.partition.manager'].sudo()._setup_partman()
