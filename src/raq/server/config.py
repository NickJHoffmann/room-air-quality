"""Config for the air quality client."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    """Config for an air quality server.
    
    Attributes:
        influxdb_token: The token for the InfluxDB server
        influxdb_url: The URL for the InfluxDB server, including the port if necessary
        influxdb_org: The organization for the InfluxDB server
        influxdb_bucket: The bucket for the InfluxDB server
        influxdb_measurement: The measurement for the InfluxDB server
    """
    model_config = SettingsConfigDict(
        env_file="server.env",
        case_sensitive=False,
    )

    influxdb_token: SecretStr
    influxdb_url: str = "http://localhost:8086"
    influxdb_org: str = "Test Org"
    influxdb_bucket: str = "Test Bucket"
    influxdb_measurement: str = "Air Quality"
