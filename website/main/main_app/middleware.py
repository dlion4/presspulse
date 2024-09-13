# middleware.py

import logging

from django.db import connections

from config.settings.create_tenant_db import format_tenant_schema_name
from website.main.main_app.models import Domain

logger = logging.getLogger(__name__)


class TenantConnectionMiddleware:
    """
    Middleware that determines the tenant based on the request's subdomain
    and dynamically connects to the tenant database.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract tenant name from subdomain
        domain_name = request.get_host().split(":")[0]  # ignore port
        try:
            tenant = Domain.objects.get(domain=domain_name).tenant
        except Domain.DoesNotExist:
            tenant = None

        if tenant:
            # Set the tenant's schema name
            if tenant.schema_name.lower() == "public":
                return self.get_response(request)

            request.tenant = tenant
            # Use the tenant's schema database for this request
            connections.databases["default"]["NAME"] = format_tenant_schema_name(
                tenant.schema_name)

        response = self.get_response(request)
        # do further processing
        logger.info(response)
        return response
