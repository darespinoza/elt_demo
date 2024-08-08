from dagster import (
    get_dagster_logger,
)

from dagster_embedded_elt.sling import (
    SlingResource, 
    sling_assets,
)

from ..resources import incremental_replication_config

# Dagster Logger
logger = get_dagster_logger()

@sling_assets(
    replication_config=incremental_replication_config,
    )
def my_sling_assets(context, 
            sling: SlingResource):
    """
        Uses a Sling resources to stream data from SQL Server source to Postgres target
    """
    try:
        yield from sling.replicate(context=context)
    except Exception as e:
        logger.error(f"[ERROR] Streaming open-meteo data with Sling.\n{str(e)}")