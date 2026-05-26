from . import models
from . import wizard


def post_init_hook(env):
    """Install pg_partman and partition accounting tables."""
    env['pg.partition.manager'].sudo()._setup_partman()
