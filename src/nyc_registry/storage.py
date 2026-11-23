"""Object storage through the S3 API only (ADR 0002): endpoint and keys come from Settings."""

import boto3
from botocore.exceptions import ClientError
from types_boto3_s3 import S3Client

from nyc_registry.config import Settings


def s3_client(settings: Settings) -> S3Client:
    """An S3 client for the configured endpoint (SeaweedFS locally, AWS later)."""
    return boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint_url,
        aws_access_key_id=settings.s3_access_key.get_secret_value(),
        aws_secret_access_key=settings.s3_secret_key.get_secret_value(),
        region_name=settings.s3_region,
    )


def ensure_bucket(client: S3Client, bucket: str) -> bool:
    """Create the bucket if it does not exist. Returns True when it was created."""
    try:
        client.head_bucket(Bucket=bucket)
    except ClientError as error:
        status = error.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status != 404:
            raise
        client.create_bucket(Bucket=bucket)
        return True
    return False
