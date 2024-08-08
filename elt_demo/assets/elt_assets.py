from dagster import (
    asset,
    AssetIn,
    AssetKey,
    IdentityPartitionMapping,
    AssetExecutionContext,
    MetadataValue,
    get_dagster_logger,
    MonthlyPartitionsDefinition,
)

from dagster_embedded_elt.sling import (
    SlingResource, 
    sling_assets,
)

import requests
import pandas as pd
from dotenv import load_dotenv
import os

from ..resources import PostgresResource, MSSQLResource, incremental_replication_config
from .constants import LATITUDE, LONGITUDE, OM_ERA5_URL, DBT_PROJ_PATH, RAW_METEO_TABLE

# Create a MonthlyPartitionDefinition for Open-Meteo asset
om_monthly_partition = MonthlyPartitionsDefinition(start_date="2024-01-01")

# Dagster Logger
logger = get_dagster_logger()

# Load environment variables from .env file
load_dotenv()

@asset(
    group_name="raw_data_collection",
    partitions_def=om_monthly_partition,
    io_manager_key="fs_io_manager",
)
def open_meteo_monthly_data(context: AssetExecutionContext) -> pd.DataFrame:
    """
        Gets monthly historical data from Open-Meteo API using a monthly partition. Selected Variables are Temperature, Wind Speed,
        Relative Humidity and Precipitation.

        https://open-meteo.com/

        Args:
            context (AssetExecutionContext): For metadata
    """

    try:
        # Get the time window for the current partition
        bounds = context.partition_time_window
        start_date = bounds.start.strftime("%Y-%m-%d")
        end_date = bounds.end.strftime("%Y-%m-%d")
        logger.info(f"Attepmting to get data from {start_date} to {end_date}, from Open-Meteo API")

        # Request parameters
        params = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "hourly": "temperature_2m,wind_speed_10m,relative_humidity_2m,precipitation",
            "start_date": f"{start_date}",
            "end_date": f"{end_date}",
        }

        # Perform the request
        response = requests.get(OM_ERA5_URL, params=params)

        # Create an empty Dataframe to save response
        df = None

        # Check request response status
        if response.status_code == 200:
            data = response.json()

            # Create a Dataframe with response's hourly data
            df = pd.DataFrame({
                "Time": data["hourly"]["time"],
                "Temperature": data["hourly"]["temperature_2m"],
                "Wind_Speed": data["hourly"]["wind_speed_10m"],
                "Relative_Humidity": data["hourly"]["relative_humidity_2m"],
                "Precipitation": data["hourly"]["precipitation"],
            })

            # Convertir la columna 'fecha' a tipo datetime
            df['Time'] = pd.to_datetime(df['Time'])
        else:
            df = pd.DataFrame()
            logger.error(f"[Error] Request error: {response.status_code}")

        # Save metadata
        context.add_output_metadata(
                metadata={
                    "rec_number": len(df),
                    "preview": MetadataValue.md(df.head().to_markdown()),
                }
            )

        return (df)
    except Exception as e:
        logger.error(f"[ERROR] Getting data from Open-Meteo.\n{str(e)}")

@asset(
    group_name="raw_data_collection",
    partitions_def=om_monthly_partition,
    io_manager_key="fs_io_manager",
    ins={
        "open_meteo_monthly_data": AssetIn(
            key=AssetKey("open_meteo_monthly_data"),
            partition_mapping=IdentityPartitionMapping()
        )
    },
)
def raw_data_save_mssql(context: AssetExecutionContext,
                        mssql_resource: MSSQLResource,
                        open_meteo_monthly_data: pd.DataFrame) -> None:
    """
        Saves collected data from upstream asset "open_meteo_monthly_data" into SQL Server DB
        using a MSSQLResource

        Args:
            context (AssetExecutionContext): For metadata
            mssql_resource (MSSQLResource): SQL Server reource
            open_meteo_monthly_data (pd.DataFrame): Upstream asset with partitioned metheorologic data.
    """
    try:
        # Use MSSQL engine to save data
        engine = mssql_resource.get_engine()

        with engine.connect() as connection:
            # Load the DataFrame into the SQL Server database
            rows_written = open_meteo_monthly_data.to_sql(RAW_METEO_TABLE, 
                                        connection, 
                                        if_exists='append', 
                                        index=False, 
                                        schema=os.getenv('MSSQL_SCHEMA'))
        engine.dispose()

        # Save metadata
        logger.info(f"{rows_written} record(s) saved on SQL Server database")
        context.add_output_metadata(
                metadata={
                    "rows_df": len(open_meteo_monthly_data),
                    "rows_written": rows_written,
                }
            )
    except Exception as e:
        logger.error(f"[ERROR] Saving data from Open-Meteo.\n{str(e)}")

@sling_assets(
    replication_config=incremental_replication_config,
    )
def my_assets(context, 
            sling: SlingResource):
    """
        Uses a Sling resources to stream data from SQL Server source to Postgres target
    """
    try:
        yield from sling.replicate(context=context)
    except Exception as e:
        logger.error(f"[ERROR] Streaming open-meteo data with Sling.\n{str(e)}")
