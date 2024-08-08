from pathlib import Path

# dbt project paths
DBT_PROJ_PATH = Path(__file__).joinpath("..", "..", "..", "demo_transformations").resolve()

# Cuenca, Ecuador
LATITUDE = -2.90055
LONGITUDE = -79.00453

# Open-Meteo API URL
OM_URL = f"https://api.open-meteo.com/v1/forecast"
OM_ERA5_URL = f"https://archive-api.open-meteo.com/v1/era5"

# MSSQL RAW DATABASE
RAW_METEO_TABLE = "raw_openmeteo_data"