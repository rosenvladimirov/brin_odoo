# Copyright 2024-2026 Rosen Vladimirov
# License AGPL-3.0-or-later (dual — see LICENSE-COMMERCIAL.md)
"""Re-run partition setup on upgrade.

post_init_hook only fires on install; when PARTITION_TARGETS gains new tables
(or start_year/interval change) an upgrade must re-run _setup_partman so the
new targets get partitioned. Idempotent: already-partitioned tables are skipped
(only run_maintenance is called for them)."""
from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['pg.partition.manager']._setup_partman()
