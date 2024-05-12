from functools import lru_cache

from pydantic import Field, BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = "../.env"
        extra = "ignore"
        case_sensitive = False

    backend_database_connection_string: str = Field(...)

    backend_service_url: str = Field(...)
    frontend_url: str = Field(...)

    strava_client_id: str = Field(...)
    strava_client_secret: str = Field(...)

    vite_session_cookie_name: str = Field(...)


_settings = Settings()


@lru_cache
def get_settings() -> Settings:
    return _settings
