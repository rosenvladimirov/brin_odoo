from . import fk_partition_patch  # installs ORM FK tolerance for partitioned tables
from . import pg_partition_manager
from . import account_move_line_partition_date  # keep partition key date non-null
