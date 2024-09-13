from django_tenants.files.storage import TenantFileSystemStorage

AWS_LOCATION = "media"  # Folder inside the S3 bucket

# Tenant-aware storage (override location)

class TenantS3Boto3Storage(TenantFileSystemStorage):
    location = AWS_LOCATION
