from django.core.management import call_command

from config.settings.create_tenant_db import create_tenant_database

from .models import Client
from .models import Domain


def create_new_tenant(name, domain_name):
    """
    Creates a new tenant with its own database and domain.
    """
    # 1. Create the tenant
    tenant = Client(schema_name=name.lower(), name=name)
    tenant.save()
    # 2. Create the tenant database
    create_tenant_database(tenant.schema_name)
    # 3. Migrate the tenant-specific schema
    call_command("migrate_schemas", schema_name=tenant.schema_name)
    # 4. Create the domain for the tenant
    domain = Domain(domain=domain_name, tenant=tenant, is_primary=True)
    domain.save()

# Example usage
create_new_tenant(name="University", domain_name="university.example.com")
create_new_tenant(name="Medical", domain_name="medical.example.com")
