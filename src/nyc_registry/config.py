"""Settings read from environment variables (and a local .env file), never hard-coded."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Connection settings for the local environment. See .env.example."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    registry_db_name: str
    registry_db_user: str
    registry_db_password: SecretStr

    s3_endpoint_url: str
    s3_access_key: SecretStr
    s3_secret_key: SecretStr
    s3_region: str = "us-east-1"
    bronze_bucket: str = "bronze"

    airflow_url: str = "http://localhost:8080"

    def postgres_conninfo(self) -> str:
        """libpq connection string for the project database."""
        return (
            f"host={self.postgres_host} port={self.postgres_port} "
            f"dbname={self.registry_db_name} user={self.registry_db_user} "
            f"password={self.registry_db_password.get_secret_value()}"
        )
