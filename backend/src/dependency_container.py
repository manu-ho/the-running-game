from dependency_injector import containers, providers
from fastapi.security import OAuth2AuthorizationCodeBearer
from src.database.database import Database
from src.database.database_operations import DatabaseOperations
from src.settings import get_settings


class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["src.endpoints", "src.data_provider"]
    )

    settings = providers.Singleton(get_settings)

    authorization_url: str = providers.Singleton(
        lambda settings: f"http://www.strava.com/oauth/authorize?client_id="
        f"{settings.strava_client_id}&response_type=code&redirect_uri="
        f"{settings.backend_service_url}/oauth/auth&approval_prompt=auto&scope="
        f"activity:read_all,profile:read_all",
        settings.provided,
    )

    _token_url = (
        (
            f"https://www.strava.com/oauth/token?client_id="
            f"{settings.provided.strava_client_id}&client_secret="
            f"{settings.provided.strava_client_secret}&grant_type=authorization_code"
        ),
    )
    _refresh_url = (
        f"https://www.strava.com/oauth/token?client_id="
        f"{settings.provided.strava_client_id}&client_secret="
        f"{settings.provided.strava_client_secret}&grant_type=refresh_token"
    )
    oauth2scheme = providers.Singleton(
        OAuth2AuthorizationCodeBearer,
        authorizationUrl=authorization_url,
        tokenUrl=_token_url,
        refreshUrl=_refresh_url,
    )

    database = providers.Singleton(
        Database, connection_string=settings.provided.backend_database_connection_string
    )
    database_operations = providers.Factory(
        DatabaseOperations,
        session_factory=database.provided.session,
    )
