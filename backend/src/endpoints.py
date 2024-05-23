import logging
from datetime import datetime, timedelta
from typing import Annotated
from uuid import uuid4

import pytz
import stravalib
import stravalib.exc
from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Cookie,
    Depends,
    HTTPException,
    Response,
    status,
)
from fastapi.responses import RedirectResponse
from src import schemas
from src.data_provider import DataProvider
from src.database.database_operations import DatabaseOperations
from src.dependency_container import DependencyContainer
from src.exceptions import DatabaseException
from src.settings import Settings

logger = logging.getLogger(__name__)

router = APIRouter()

access_token = ""
refresh_token = ""


@inject
def handle_strava_auth_token_response(
    token_response: dict,
    background_tasks: BackgroundTasks,
    database_operations: DatabaseOperations = Depends(
        Provide[DependencyContainer.database_operations]
    ),
    settings: Settings = Depends(Provide[DependencyContainer.settings]),
) -> str:
    global access_token, refresh_token

    # TODO save access_token, ?refresh_token and expires_at in database using state as id
    logger.info(token_response)
    access_token = token_response["access_token"]
    expires_at = token_response["expires_at"]
    refresh_token = token_response.get("refresh_token", None)

    athlete = stravalib.Client(access_token=access_token).get_athlete()

    session_id = str(uuid4())
    _ = database_operations.add_session_token(
        session_id=session_id,
        access_token=access_token,
        expires_at=expires_at,
        refresh_token=refresh_token,
        athlete=athlete,
    )

    # FIXME: generate a token from the session id instead of the session id directly
    return session_id


def get_strava_client(
    session_id: Annotated[str, Cookie(alias="therunninggame_sessionid")],
) -> stravalib.Client:
    try:
        return DataProvider(session_id=session_id).get_strava_client()
    except DatabaseException as e:
        raise HTTPException(status_code=e.error_code, detail=str(e))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No valid token provided."
        )


@router.get("/login")
@inject
async def login(
    authorization_url: str = Depends(Provide[DependencyContainer.authorization_url]),
):
    return schemas.LoginUrl(authorization_url=str(authorization_url))


@router.get("/oauth/auth")
@inject
async def authorization_code(
    background_tasks: BackgroundTasks,
    code: str | None = None,
    error: str | None = None,
    settings: Settings = Depends(Provide[DependencyContainer.settings]),
):
    if error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        token_response = stravalib.Client().exchange_code_for_token(
            client_id=settings.strava_client_id,
            client_secret=settings.strava_client_secret,
            code=code,
        )
    except stravalib.exc.Fault as e:
        logger.error(f"Could not exchange authorization code for token. Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    session_cookie = handle_strava_auth_token_response(token_response, background_tasks)
    # redirect user to home and set session cookie
    response = RedirectResponse(url=settings.frontend_url)
    response.set_cookie(key=settings.vite_session_cookie_name, value=session_cookie)
    return response


@router.post("/oauth/refresh")
@inject
async def refresh(
    background_tasks: BackgroundTasks,
    response: Response,
    strava_client: stravalib.Client = Depends(get_strava_client),
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    session_cookie = handle_strava_auth_token_response(token_response, background_tasks)
    # set new session cookie in response
    response.set_cookie(key=settings.vite_session_cookie_name, value=session_cookie)
    return schemas.RefreshTokenResponse(
        success=True, expiration_date=datetime.now() - timedelta(days=1)
    )


@router.get("/athlete")
@inject
async def get_athlete_info(
    session_id: Annotated[str, Cookie(alias="therunninggame_sessionid")],
) -> schemas.Athlete:
    data_provider = DataProvider(session_id=session_id)
    try:
        user = data_provider.get_user(session_id)
    except DatabaseException as e:
        raise HTTPException(status_code=e.error_code, detail=str(e))
    return schemas.Athlete.from_orm(user)


@router.get("/activities")
@inject
async def get_activities(
    session_id: Annotated[str, Cookie(alias="therunninggame_sessionid")],
    after: datetime | None = None,
    before: datetime | None = None,
) -> list[schemas.Activity]:
    if after is None:
        after = datetime.now() - timedelta(weeks=4)
    if before is None:
        before = datetime.now()
    if before.replace(tzinfo=pytz.UTC) > datetime.now(pytz.UTC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Before must be earlier than current time. "
                f"Got: {before} wich is {before-datetime.now()} ahead of time."
            ),
        )

    data_provider = DataProvider(session_id=session_id)

    try:
        activities = data_provider.get_activities(after=after, before=before)
    except DatabaseException as e:
        raise HTTPException(status_code=e.error_code, detail=str(e))

    return activities
