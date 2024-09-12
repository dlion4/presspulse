import logging

from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand
from config.settings.base import add_tenant_database
from config.settings.create_tenant_db import create_tenant_database, format_tenant_schema_name
from website.main.main_app.models import Client
from website.main.main_app.models import Domain

logger = logging.getLogger(__file__)

class Command(BaseCommand):
    help = "Creates a new tenant with its own database and domain."

    def add_arguments(self, parser):
        # Positional argument for schema name (tenant name)
        parser.add_argument(
            "schema_name", type=str, help="Schema name of the new tenant")

    def handle(self, *args, **kwargs):
        schema_name = kwargs["schema_name"].lower()

        # Get the current site (main domain)
        site = Site.objects.get_current()
        main_domain = site.domain

        # Form the tenant's domain by appending the schema name to the main domain
        tenant_domain = f"{schema_name}.{main_domain}"

        # Call the function to create the new tenant
        create_new_tenant(schema_name, tenant_domain)

        self.stdout.write(
            self.style.SUCCESS(
                f"""
                Successfully created tenant
                '{schema_name}' with domain '{tenant_domain}'
                """))

def create_new_tenant(schema_name:str, domain_name:str):
    """
    Creates a new tenant with its own database and domain.
    """
    # 1. Create the tenant
    tenant:Client = Client(schema_name=schema_name, name=schema_name.capitalize())
    tenant.save()
    # 2. Create the tenant database
    create_tenant_database(tenant.schema_name)
    # 3. Add tenant database to Django's DATABASES
    add_tenant_database(format_tenant_schema_name(tenant.schema_name))
    # 3. Migrate the tenant-specific schema
    call_command("migrate_schemas", schema_name=tenant.schema_name)
    # also makemigrations and then migrate migrate the entire db
    call_command(
        "makemigrations", f"--database={format_tenant_schema_name(tenant.schema_name)}")
    call_command(
        "migrate", f"--database={format_tenant_schema_name(tenant.schema_name)}")

    # 4. Create the domain for the tenant
    domain = Domain(domain=domain_name, tenant=tenant, is_primary=True)
    domain.save()
    logger.info("Tenant '%s' created with domain '%s'", schema_name, domain_name)
