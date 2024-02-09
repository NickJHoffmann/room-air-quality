from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    influxdb_token: SecretStr
    influxdb_url: str = "http://localhost:8086"
    influxdb_org: str = "Test Org"
    influxdb_bucket: str = "Test Bucket"
    influxdb_measurement: str = "Air Quality"
