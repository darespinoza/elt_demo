from dagster import (
    ScheduleDefinition, 
    build_schedule_from_partitioned_job,
)
from ..jobs import dbt_job, sling_job #, monthly_asset_job

dbt_schedule = ScheduleDefinition(
    job=dbt_job,
    cron_schedule="0 2 1 * *", # At 02:00 on day-of-month 1.
)

# Define a schedule that runs the job every day at midnight
sling_schedule = ScheduleDefinition(
    job=sling_job,
    cron_schedule="0 1 1 * *", # At 01:00 on day-of-month 1.
)

# Define a schedule that runs the job at the start of each month
# monthly_asset_schedule = build_schedule_from_partitioned_job(
#     monthly_asset_job,
#     name="monthly_asset_schedule",
#     cron_schedule="0 0 1 * *",  # At midnight on the first day of each month
# )