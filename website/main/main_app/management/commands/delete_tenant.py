from django.core.management import call_command
from django.core.management.base import BaseCommand

from config.settings.drop_tenant_db import drop_tenant_database
from website.main.main_app.models import Client
from website.main.main_app.models import Domain

# Add a function to drop the database

class Command(BaseCommand):
    help = "Deletes an existing tenant by schema name."

    def add_arguments(self, parser):
        # Positional argument for schema name (tenant name)
        parser.add_argument(
            "schema_name", type=str, help="Schema name of the tenant to delete")

    def handle(self, *args, **kwargs):
        schema_name = kwargs["schema_name"].lower()
        try:
            # 1. Retrieve the tenant
            tenant = Client.objects.get(schema_name=schema_name)
            # 2. Drop the tenant database
            drop_tenant_database(tenant.schema_name)
            # 3. Delete the domain associated with this tenant
            Domain.objects.filter(tenant=tenant).delete()
            # 4. Delete the tenant itself
            tenant.delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully deleted tenant '{schema_name}' and its domain."))

        except Client.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f"Tenant with schema name '{schema_name}' does not exist."))
