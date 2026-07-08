{
    'name': 'PostgreSQL Table Partitioning',
    'version': '19.0.1.0.0',
    'summary': 'Declarative PostgreSQL partitioning for large Odoo tables using pg_partman',
    'description': """
PostgreSQL Table Partitioning
=============================
Installs pg_partman extension and configures RANGE partitioning
for large Odoo accounting and stock tables.

Features:
- Auto-installs pg_partman schema and extension
- Partitions account_move_line by date (yearly)
- Partitions stock_move by date (yearly)
- Wizard for pg_dump backup of individual partitions
- Dashboard showing partition sizes and row counts

Requirements:
- PostgreSQL 16+
- pg_partman installed on the server (postgresql-16-partman)
""",
    'author': 'Rosen Vladimirov',
    'website': 'https://github.com/rosenvladimirov/brin_odoo',
    'license': 'AGPL-3',
    'category': 'Technical',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/pg_partition_data.xml',
        'wizard/partition_backup_wizard_views.xml',
        'views/pg_partition_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'post_load': 'post_load',
    'auto_install': False,
    'installable': True,
}
