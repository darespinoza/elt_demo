from dagster import (
    ConfigurableResource,
    get_dagster_logger,
)
from dagster_embedded_elt.sling import (
    SlingConnectionResource,
    SlingResource,
)
from dagster_dbt import DbtCliResource
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
import os

from ..assets.constants import DBT_PROJ_PATH, RAW_METEO_TABLE

# dbt resource to perform demo tranformations
dbt_resource = DbtCliResource(
    project_dir=DBT_PROJ_PATH,
)

# Load environment variables from .env file
# load_dotenv()

# Get Dagster Logger
logger = get_dagster_logger()

# Customized ConfigurableResource for Postgres resource
class PostgresResource(ConfigurableResource):
    """
    A custom resource for connecting to a PostgreSQL database using SQLAlchemy.
    """
    
    try:
        username: str
        password: str
        hostname: str
        db_name: str
        port: int

        def get_engine(self) -> Engine:
            connection_uri = f"postgresql://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.db_name}"
            return create_engine(connection_uri)
    
    except Exception as e:
        logger.error(f"Error while creating PostgreSQL Resource.\n{str(e)}")

# Postgres dbt resource instansce
postgres_resource = PostgresResource(
    username=os.getenv('PG_USER'),
    password=os.getenv('PG_PASSWORD'),
    hostname=os.getenv('PG_HOST'),
    db_name=os.getenv('PG_DATABASE'),
    port=int(os.getenv('PG_PORT')),
)

# Customized ConfigurableResource for MSSQL resource
class MSSQLResource(ConfigurableResource):
    """
    A custom resource for connecting to a SQL Server 2017 database using SQLAlchemy.
    """
    try:
        username: str
        password: str
        hostname: str
        db_name: str
        port: int
        driver: str

        def get_engine(self) -> Engine:
            connection_uri = f"mssql+pyodbc://{self.username}:{self.password}@{self.hostname},{self.port}/{self.db_name}?driver={self.driver}"
            return create_engine(connection_uri)
    except Exception as e:
        logger.error(f"Error while creating MSSQL Resource.\n{str(e)}")

# MSSQL resource instance
mssql_resource = MSSQLResource(
    username=os.getenv('MSSQL_USER'),
    password=os.getenv('MSSQL_PASSWORD'),
    hostname=os.getenv('MSSQL_HOST'),
    db_name=os.getenv('MSSQL_DATABASE'),
    port=int(os.getenv('MSSQL_PORT')),
    driver=os.getenv('MSSQL_DRIVER'),
)

# Sling resource declaration
sling_resource = SlingResource(
    connections=[
        # Sling MSSQL Connection
        SlingConnectionResource(
            name="MY_MSSQL_SOURCE",
            type="sqlserver",
            connection_string=f"sqlserver://{os.getenv('MSSQL_USER')}:{os.getenv('MSSQL_PASSWORD')}@{os.getenv('MSSQL_HOST')}:{int(os.getenv('MSSQL_PORT'))}/{os.getenv('MSSQL_DATABASE')}?driver={os.getenv('MSSQL_DRIVER')}",
        ),
        # Sling Postgres Connection
        SlingConnectionResource(
            name="MY_PG_TARGET",
            type="postgres",
            connection_string=f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}:{int(os.getenv('PG_PORT'))}/{os.getenv('PG_DATABASE')}?sslmode=disable",
        ),
    ]
)

# Sling incremental replication config
incremental_replication_config = {
    "source": "MY_MSSQL_SOURCE",
    "target": "MY_PG_TARGET",
    "defaults": {"mode": "incremental", "object": "public.{stream_table}"},
    "streams": {
        f"{os.getenv('MSSQL_SCHEMA')}.{RAW_METEO_TABLE}": {
            "mode": "incremental", 
            "update_key": "Time",
            "object": f"{os.getenv('PG_SCHEMA')}.{RAW_METEO_TABLE}" },
    },
}

