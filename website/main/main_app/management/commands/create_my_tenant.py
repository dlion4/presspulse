import logging
import time

from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from django_tenants.utils import schema_context

from config.settings.base import add_tenant_database
from config.settings.create_tenant_db import create_tenant_database
from config.settings.create_tenant_db import format_tenant_schema_name
from website.main.main_app.models import Client
from website.main.main_app.models import Domain

logger = logging.getLogger(__file__)

class Command(BaseCommand):
    help = "Creates a new tenant with its own database and domain."
    """ # Create My Tenant Management Command

        ## Overview
        This Django management command creates a new tenant with its own database and domain in a multi-tenant application.

        ## Usage
        ### Arguments
        - `schema_name`: (Required) The name of the new tenant's schema.
        - `--database`: (Optional) The name of the database to use. Defaults to "default".

        ## Functionality
        1. Creates a new `Client` instance (tenant) with the given schema name.
        2. Creates a new database for the tenant.
        3. Adds the tenant's database to Django's `DATABASES` setting.
        4. Runs migrations for the tenant's schema.
        5. Creates a new `Domain` instance for the tenant.

        ## Example
        This creates a new tenant named "finance" using the "tenant_db" database.

        ## Notes
        - The tenant's domain will be created as a subdomain of the current site's domain.
        - Logging is implemented to track tenant creation.
        - Ensure proper database configurations are in place before running this command.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "schema_name", type=str, help="Schema name of the new tenant")

    def handle(self, *args, **options):
        schema_name = options["schema_name"].lower()

        site = Site.objects.get_current()
        main_domain = site.domain
        tenant_domain = f"{schema_name}.{main_domain}"

        create_new_tenant(schema_name, tenant_domain)

        self.stdout.write(
            self.style.SUCCESS(
                f"""
                Successfully created
                tenant '{schema_name}' with domain '{tenant_domain}'
                """,
            ),
        )

def create_new_tenant(schema_name: str, domain_name: str):
    tenant:Client = Client(schema_name=schema_name, name=schema_name.capitalize())
    tenant.save()

    create_tenant_database(tenant.schema_name)
    add_tenant_database(format_tenant_schema_name(tenant.schema_name))

    tenant_db = format_tenant_schema_name(tenant.schema_name)
    # Ensure the connection is properly set up
    max_retries = 5
    for attempt in range(max_retries):
        try:
            connections[tenant_db].ensure_connection()
            break
        except OperationalError:
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait for 1 second before retrying
            else:
                raise  # Re-raise the last exception if all retries failed
    # Create the schema
    with connections[tenant_db].cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {tenant.schema_name}")

    # Create schema and run migrations within the correct schema context
    with schema_context(tenant.schema_name):
        # Run migrations
        call_command("migrate_schemas", schema_name=tenant.schema_name, verbosity=0)

    domain:Domain = Domain(domain=domain_name, tenant=tenant, is_primary=True)
    domain.save()

    logger.info(
        "Tenant '%s' created with domain '%s'",
        schema_name, domain_name)
