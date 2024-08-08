from dagster import (
    AssetExecutionContext,
    get_dagster_logger,
)

from dagster_dbt import (
    dbt_assets, 
    DbtCliResource,
)

from ..resources import dbt_resource
from .constants import DBT_PROJ_PATH

import os

# Dagster Logger
logger = get_dagster_logger()

# Get dbt manifest
if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
    dbt_manifest_path = (
        dbt_resource.cli(["--quiet", "parse"])
        .wait()
        .target_path.joinpath("manifest.json")
    )
else:
    dbt_manifest_path = os.path.join(DBT_PROJ_PATH, "target", "manifest.json")

@dbt_assets(
    manifest=dbt_manifest_path,
)
def dbt_demo_models(context: AssetExecutionContext, 
                dbt_resource: DbtCliResource):
    try:
        yield from dbt_resource.cli(["build"], context=context).stream()
    except Exception as e:
        logger.error(f"[ERROR] Running dbt models.\n{str(e)}")