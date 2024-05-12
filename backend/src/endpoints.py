import logging
from datetime import datetime, timedelta
from typing import Annotated
from uuid import uuid4

import stravalib
import stravalib.exc
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from src.database_operations import DatabaseOperations
from src.dependency_container import DependencyContainer
from src.schemas import LoginUrl, RefreshTokenResponse
from src.settings import Settings
from stravalib import Client
from stravalib.model import Activity, Athlete

logger = logging.getLogger(__name__)

router = APIRouter()

access_token = ""
refresh_token = ""


@inject
def handle_token_response(
    response: dict,
    database_operations: DatabaseOperations = Depends(
        Provide[DependencyContainer.database_operations]
    ),
    settings: Settings = Depends(Provide[DependencyContainer.settings]),
) -> str:
    global access_token, refresh_token

    # TODO save access_token, ?refresh_token and expires_at in database using state as id
    logger.info(response)
    access_token = response["access_token"]
    expires_at = response["expires_at"]
    refresh_token = response.get("refresh_token", None)

    session_id = str(uuid4())
    _ = database_operations.add_session_token(
        session_id=session_id,
        access_token=access_token,
        expires_at=expires_at,
        refresh_token=refresh_token,
    )

    # FIXME: generate a token from the session id instead of the session id directly
    return session_id


@inject
def get_strava_client(
    session_id: Annotated[str, Cookie(alias="therunninggame_sessionid")],
    database_operations: DatabaseOperations = Depends(
        Provide[DependencyContainer.database_operations]
    ),
) -> Client:
    client_session = database_operations.get_session_token(sesstion_id=session_id)
    token = client_session.access_token
    if token:
        return Client(access_token=token)
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="No valid token provided."
    )


@router.get("/login")
@inject
async def login(
    authorization_url: str = Depends(Provide[DependencyContainer.authorization_url]),
):
    return LoginUrl(authorization_url=str(authorization_url))


@router.get("/oauth/auth")
@inject
async def authorization_code(
    code: str | None = None,
    error: str | None = None,
    settings: Settings = Depends(Provide[DependencyContainer.settings]),
):

    if error:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        token_response = Client().exchange_code_for_token(
            client_id=settings.strava_client_id,
            client_secret=settings.strava_client_secret,
            code=code,
        )
    except stravalib.exc.Fault as e:
        logger.error(f"Could not exchange authorization code for token. Error: {e}")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    session_cookie = handle_token_response(token_response)
    # redirect user to home and set bearer token
    response = RedirectResponse(url=settings.frontend_url)
    response.set_cookie(key=settings.vite_session_cookie_name, value=session_cookie)
    return response


@router.post("/oauth/refresh")
@inject
async def refresh(
    response: Response,
    strava_client: Client = Depends(get_strava_client),
    settings: Settings = Depends(Provide[DependencyContainer.settings]),
):
    try:
        token_response = strava_client.refresh_access_token(
            client_id=settings.strava_client_id,
            client_secret=settings.strava_client_secret,
            refresh_token=refresh_token,
        )
    except stravalib.exc.Fault as e:
        logger.error(f"Could not refresh token. Error: {e}")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    session_cookie = handle_token_response(token_response)
    # set new session cookie in response
    response.set_cookie(key=settings.vite_session_cookie_name, value=session_cookie)
    return RefreshTokenResponse(
        success=True, expiration_date=datetime.now() - timedelta(days=1)
    )


@router.get("/activities")
async def get_activities(
    strava_client: Client = Depends(get_strava_client),
) -> list[Activity]:
    activities = strava_client.get_activities(limit=3)
    return list(activities)


@router.get("/athlete")
async def get_athlete_info(
    strava_client: Client = Depends(get_strava_client),
) -> Athlete:
    athlete = strava_client.get_athlete()
    return athlete
