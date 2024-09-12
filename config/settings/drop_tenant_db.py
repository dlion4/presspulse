import logging

from django.db import connection

from .create_tenant_db import format_tenant_schema_name

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

def drop_tenant_database(raw_schema_name):
    tenant_schema_name = format_tenant_schema_name(raw_schema_name)
    with connection.cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {tenant_schema_name};")
        logger.info("Database %s dropped.", tenant_schema_name)
