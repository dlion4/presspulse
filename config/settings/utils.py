from pathlib import Path

import environ

env = environ.Env()
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
env.read_env(str(BASE_DIR / ".env"))


def get_database_config(tenant_schema_name):
    return {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": tenant_schema_name,  # Use tenant's schema name as the database name
        "USER": env.str("POSTGRES_USER", "postgres"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST", "localhost"),
        "PORT": env.str("POSTGRES_PORT", "5432"),
        "ATOMIC_REQUESTS": True,
    }
