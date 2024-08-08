from dagster import (Definitions, 
                    load_assets_from_modules,
                    FilesystemIOManager,)

from .assets import elt_assets
from .resources import mssql_resource, postgres_resource, sling_resource

all_assets = load_assets_from_modules([elt_assets])

# File system IO Manager
fs_io_manager = FilesystemIOManager(
    base_dir="io_manager_data",
)

defs = Definitions(
    assets=[*all_assets],
    resources={
        "fs_io_manager": fs_io_manager,
        "mssql_resource": mssql_resource,
        "postgres_resource": postgres_resource,
        "sling": sling_resource,
    },
)
