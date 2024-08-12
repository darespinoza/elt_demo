from dagster import (
    define_asset_job, 
    AssetSelection,
    load_assets_from_modules,
)
from dagster_dbt import build_dbt_asset_selection

from ..assets.dbt_assets import dbt_demo_models
from ..assets.sling_assets import my_sling_assets
from ..assets.raw_data_assets import raw_data_save_mssql, open_meteo_monthly_data, om_monthly_partition

# Select dbt asset models downstream
dbt_selection = build_dbt_asset_selection([dbt_demo_models]).downstream()

# Select raw data assets
# raw_assets = load_assets_from_modules([raw_data_assets])

# Define dbt job
dbt_job = define_asset_job(
    name="dbt_job",
    selection=dbt_selection,
)

# Define Sling job
sling_job = define_asset_job(
    name="sling_job", 
    selection=[my_sling_assets]
)

# Define a job for the partitioned raw assets
raw_assets_job = define_asset_job(
    name="raw_assets_job",
    selection=AssetSelection.assets(raw_data_save_mssql, open_meteo_monthly_data),
    partitions_def=om_monthly_partition,
)
