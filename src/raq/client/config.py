"""Config for the air quality client."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class ClientSettings(BaseSettings):
    """Config for an air quality client.

    Attributes:
        ingress_server_url: str: The URL for the server, including the port if necessary
        room_id: str: The ID of the room the client is sending data for
    """
    model_config = SettingsConfigDict(
        env_file="client.env",
        case_sensitive=False,
    )

    ingress_server_url: str = "http://localhost:8080"
    room_id: str
