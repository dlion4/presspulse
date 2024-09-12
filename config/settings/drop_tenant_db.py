import contextlib
import logging

from django.db import connection

from .create_tenant_db import format_tenant_schema_name

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

def drop_tenant_database(raw_schema_name:str)->None:
    """
    Attempt to drop the tenant database associated with the given raw schema name.

    This function performs the following steps:
    1. Formats the raw schema name using the format_tenant_schema_name function.
    2. Establishes a database connection using a context manager.
    3. Executes a SQL command to drop the database if it exists.
    4. Logs the successful dropping of the database.
    5. Suppresses any exceptions that might occur during the process.

    Parameters:
    raw_schema_name (str): The unformatted name of the tenant's schema.

    Returns:
    None

    Note:
    - This function uses contextlib.suppress to ignore any exceptions.
    - The DROP DATABASE command is executed with IF EXISTS to prevent errors if
    the database doesn't exist.
    - Logging is performed using the logger.info method to record the successful
    operation.
    - The function assumes the existence of a format_tenant_schema_name function, a
    database connection object,
      and a configured logger.

    Caution:
    - This operation is irreversible and will permanently delete all data in the
    specified database.
    - Ensure proper backups are in place before calling this function.
    - Be aware that suppressing all exceptions might hide important errors or issues.
    """
    tenant_schema_name = format_tenant_schema_name(raw_schema_name)
    with connection.cursor() as cursor, contextlib.suppress(Exception):
        cursor.execute(f"DROP DATABASE IF EXISTS {tenant_schema_name};")
        logger.info("Database %s dropped.", tenant_schema_name)


