from pydantic_settings import BaseSettings, SettingsConfigDict


class ClientSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="client.env",
        case_sensitive=False,
    )

    ingress_server_url: str = "http://localhost:8080"
    room_id: str
