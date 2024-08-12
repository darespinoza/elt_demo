from dagster import (Definitions, 
                    load_assets_from_modules,
                    FilesystemIOManager,)

from .assets import raw_data_assets, dbt_assets, sling_assets
from .resources import mssql_resource, postgres_resource, sling_resource, dbt_resource
from .jobs import dbt_job, sling_job, raw_assets_job
from .schedules import dbt_schedule, sling_schedule, raw_asset_schedule

# Load all assets from module
all_raw_assets = load_assets_from_modules([raw_data_assets])
all_dbt_assets = load_assets_from_modules([dbt_assets])
all_sling_assets = load_assets_from_modules([sling_assets])

# Put together jobs
all_jobs = [dbt_job, sling_job, raw_assets_job]

# Put together schedules
all_schedules = [dbt_schedule, sling_schedule, raw_asset_schedule]

# File system IO Manager
fs_io_manager = FilesystemIOManager(
    base_dir="io_manager_data",
)

defs = Definitions(
    assets=[*all_raw_assets, *all_dbt_assets, *all_sling_assets],
    resources={
        "fs_io_manager": fs_io_manager,
        "mssql_resource": mssql_resource,
        "postgres_resource": postgres_resource,
        "sling": sling_resource,
        "dbt_resource": dbt_resource,
    },
    jobs=all_jobs,
    schedules=all_schedules,
)
