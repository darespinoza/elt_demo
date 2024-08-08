from setuptools import find_packages, setup

setup(
    name="celec_elt",
    packages=find_packages(exclude=["celec_elt_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dagster-postgres",
        "dagster-embedded-elt",
        "dbt-postgres",
        "pandas",
        "sqlalchemy",
        "python-dotenv",
        "psycopg2",
        "pyodbc",
        "requests",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
