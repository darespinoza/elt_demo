from dagster import (
    define_asset_job, 
    AssetSelection,
)
from dagster_dbt import build_dbt_asset_selection

from ..assets.dbt_assets import dbt_demo_models
from ..assets.sling_assets import my_sling_assets
from ..assets import raw_data_assets

# Select dbt asset models downstream
dbt_selection = build_dbt_asset_selection([dbt_demo_models]).downstream()

# Select Sling assets
# raw_assets = load_assets_from_package_module(raw_data_assets)

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

# Define a job that materializes the monthly partitioned assets
# monthly_asset_job = define_asset_job(
#     name="monthly_asset_job", 
#     selection=[raw_assets]
# )