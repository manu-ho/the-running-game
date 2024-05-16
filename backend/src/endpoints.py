import logging
from datetime import datetime, timedelta
import pytz
from typing import Annotated
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
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
from src.database_operations import DatabaseOperations
from src.dependency_container import DependencyContainer
from src.models import Session, User, Activity
from src.schemas import LoginUrl, RefreshTokenResponse, Athlete
from src.settings import Settings
from stravalib import Client
from stravalib.model import Activity

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

    athlete = Client(access_token=access_token).get_athlete()

    session_id = str(uuid4())
    _ = database_operations.add_session_token(
        session_id=session_id,
        access_token=access_token,
        expires_at=expires_at,
        refresh_token=refresh_token,
        user=athlete,
    )

    # FIXME: generate a token from the session id instead of the session id directly
    return session_id


@inject
def get_session(
    session_id: Annotated[str, Cookie(alias="therunninggame_sessionid")],
    database_operations: DatabaseOperations = Depends(
        Provide[DependencyContainer.database_operations]
    ),
) -> Session:
    try:
        return database_operations.get_session(session_id=session_id)
    except SQLAlchemyError as e:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not get session from database. {e}",
        )


def get_strava_client(
    session_id: Annotated[str, Cookie(alias="therunninggame_sessionid")],
) -> Client:
    client_session = get_session(session_id)
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
    background_tasks: BackgroundTasks,
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

    session_cookie = handle_strava_auth_token_response(token_response, background_tasks)
    # set new session cookie in response
    response.set_cookie(key=settings.vite_session_cookie_name, value=session_cookie)
    return RefreshTokenResponse(
        success=True, expiration_date=datetime.now() - timedelta(days=1)
    )


@router.get("/athlete")
@inject
async def get_athlete_info(
    session_id: Annotated[str, Cookie(alias="therunninggame_sessionid")],
    database_operations: DatabaseOperations = Depends(
        Provide[DependencyContainer.database_operations]
    ),
) -> Athlete:
    try:
        user = database_operations.get_user(session_id)
    except SQLAlchemyError as e:
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not get user from database. {e}",
        )
    return Athlete.from_orm(user)


@router.get("/activities")
@inject
async def get_activities(
    session_id: Annotated[str, Cookie(alias="therunninggame_sessionid")],
    after: datetime | None = None,
    before: datetime | None = None,
    database_operations: DatabaseOperations = Depends(
        Provide[DependencyContainer.database_operations]
    ),
    # strava_client: Client = Depends(get_strava_client),
) -> list[Activity]:
    if after is None:
        after = datetime.now() - timedelta(weeks=4)
    if before is None:
        before = datetime.now()
    if before > datetime.now():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Before must be earlier than current time. "
                f"Got: {before} wich is {before-datetime.now()} ahead of time."
            ),
        )
    after = after.replace(tzinfo=pytz.UTC)
    before = before.replace(tzinfo=pytz.UTC)

    try:
        user = database_operations.get_user(session_id=session_id)
        # pre_loaded_activity_timerange = (
        #     database_operations.get_activity_timerange_present(user=user)
        # )  # TODO keep track of ingested data dateranges
        pre_loaded_activity_timerange = (
            datetime.now().replace(tzinfo=pytz.UTC),
            (datetime.now() - timedelta(weeks=4)).replace(tzinfo=pytz.UTC),
        )
        if after < pre_loaded_activity_timerange[0]:
            load_activities_from_strava(
                session_id=session_id,
                user=user,
                after=after,
                before=pre_loaded_activity_timerange[0],
            )
        if pre_loaded_activity_timerange[1] < before:
            load_activities_from_strava(
                session_id=session_id,
                user=user,
                after=pre_loaded_activity_timerange[0],
                before=before,
            )
        activities = database_operations.get_activities(
            user=user, before=before, after=after
        )
    except SQLAlchemyError as e:
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not get activities from database. {e}",
        )
    return [Activity.from_orm(act) for act in activities]
    # activities = strava_client.get_activities(limit=3)
    # return list(activities)


@inject
def load_activities_from_strava(
    session_id: str,
    user: User,
    after: datetime,
    before: datetime,
    database_operations: DatabaseOperations = Depends(
        Provide[DependencyContainer.database_operations]
    ),
):
    strava_client = get_strava_client(session_id=session_id)
    activities = strava_client.get_activities(
        after=after,
        before=before,
    )
    database_operations.insert_activities(
        user=user,
        activities=activities,
    )
