import logging
import re
from urllib.parse import quote_plus

import psycopg2
from django.conf import settings
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def format_tenant_schema_name(raw_schema_name):
    """
    Cleans and formats the tenant schema name by:
    - Stripping leading/trailing spaces
    - Replacing spaces with underscores
    - Making it URL-safe
    - Lowercasing the name
    """
    # Replace spaces with underscores and strip leading/trailing spaces
    cleaned_name = re.sub(r"\s+", "_", raw_schema_name.strip())
    # Make URL-safe and lowercase
    return quote_plus(cleaned_name).lower()


def create_tenant_database(raw_schema_name):
    """
    Creates a database for the tenant with the given schema name if it
    does not already exist.
    """
    tenant_schema_name = format_tenant_schema_name(raw_schema_name)
    conn = psycopg2.connect(
        dbname="postgres",  # Connect to the default 'postgres' DB first
        user=settings.DATABASES["default"]["USER"],
        password=settings.DATABASES["default"]["PASSWORD"],
        host=settings.DATABASES["default"]["HOST"],
        port=settings.DATABASES["default"]["PORT"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # Check if the database already exists
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s", (tenant_schema_name,))
    exists = cursor.fetchone()

    if not exists:
        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE {tenant_schema_name}")
        logging.info(f"Database '{tenant_schema_name}' created successfully.")  # noqa: G004
    else:
        logging.warning(f"Database '{tenant_schema_name}' already exists.")  # noqa: G004

    cursor.close()
    conn.close()
