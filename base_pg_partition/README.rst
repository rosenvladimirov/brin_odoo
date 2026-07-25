=====================================
PostgreSQL Table Partitioning for Odoo
=====================================

Requirements
------------
- PostgreSQL 16+
- pg_partman installed on the server::

    apt install postgresql-16-partman

- In postgresql.conf::

    shared_preload_libraries = 'pg_partman_bgw'
    pg_partman_bgw.interval = 3600
    pg_partman_bgw.dbname = your_db

Installation
------------
1. Install system package: ``apt install postgresql-16-partman``
2. Restart PostgreSQL
3. Install module in Odoo

On install, the module will:

- Create ``partman`` schema
- Install ``pg_partman`` extension
- Convert ``account_move_line`` to RANGE partitioned by date (yearly)
- Convert ``stock_move`` to RANGE partitioned by date (yearly)

.. warning::
   Conversion requires renaming and copying the original table.
   Run during a maintenance window on production databases.
   On a 500K row table (~Мек Електроникс), expect 2-5 minutes.

Backup
------
Settings → PG Partitions → Backup Partition

Select a partition (e.g. ``account_move_line_p2023``) and specify
output directory. The wizard runs::

    pg_dump --format=custom --compress=9 \
            --table=account_move_line_p2023 \
            --file=/tmp/odoo_account_move_line_p2023_20260315.dump \
            your_db

Maintenance
-----------
A weekly cron job runs ``partman.run_maintenance()`` which pre-creates
the next year's partition automatically.

Manual trigger::

    Settings → PG Partitions → Backup Partition → Run Maintenance

Contributors
------------
- Rosen Vladimirov <vladimirov.rosen@odoo-shell.dev>
