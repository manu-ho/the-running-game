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
from src.exceptions import DatabaseException
from src.models import Session, User, Activity
from src import schemas
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
        athlete=athlete,
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
        raise HTTPException(
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
        token_response = Client().exchange_code_for_token(
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
    database_operations: DatabaseOperations = Depends(
        Provide[DependencyContainer.database_operations]
    ),
) -> schemas.Athlete:
    try:
        user = database_operations.get_user(session_id)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not get user from database. {e}",
        )
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

    try:
        activities = get_activities(session_id=session_id, after=after, before=before)
    except DatabaseException as e:
        raise HTTPException(status_code=e.error_code, detail=str(e))

    return activities


@inject
def get_activities(
    session_id: str,
    after: datetime,
    before: datetime,
    database_operations: DatabaseOperations = Depends(
        Provide[DependencyContainer.database_operations]
    ),
) -> list[schemas.Activity]:
    try:
        user = database_operations.get_user(session_id=session_id)
        if user is None:
            raise DatabaseException(
                error_code=status.HTTP_404_NOT_FOUND,
                message=f"Could not get user for session {session_id}",
            )
        _pull_activities_from_strava_into_database(
            session_id=session_id,
            user=user,
            after=after,
            before=before,
            database_operations=database_operations,
        )
        activities = database_operations.get_activities(
            user=user, after=after, before=before
        )
    except SQLAlchemyError as e:
        raise DatabaseException(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Could not update and get activities in database. {e}",
        )
    activities = [schemas.Activity.from_orm(act) for act in activities]
    return activities


def _pull_activities_from_strava_into_database(
    session_id: str,
    user: User,
    after: datetime,
    before: datetime,
    database_operations: DatabaseOperations,
) -> None:
    after = after.replace(tzinfo=pytz.UTC)
    before = before.replace(tzinfo=pytz.UTC)
    pre_loaded_activity_timerange = database_operations.get_activity_timerange_present(
        user=user
    )
    logger.info(
        f"Found activity data between {pre_loaded_activity_timerange[0]} and "
        f"{pre_loaded_activity_timerange[1]} in database."
    )
    if (
        pre_loaded_activity_timerange[0] is None
        or pre_loaded_activity_timerange[1] is None
    ):
        _ingest_activities_from_strava(
            session_id=session_id,
            user=user,
            after=after,
            before=before,
            database_operations=database_operations,
        )
        return
    if after < pre_loaded_activity_timerange[0]:
        _ingest_activities_from_strava(
            session_id=session_id,
            user=user,
            after=after,
            before=pre_loaded_activity_timerange[0],
            database_operations=database_operations,
        )
    if pre_loaded_activity_timerange[1] < before:
        _ingest_activities_from_strava(
            session_id=session_id,
            user=user,
            after=pre_loaded_activity_timerange[1],
            before=before,
            database_operations=database_operations,
        )


def _ingest_activities_from_strava(
    session_id: str,
    user: User,
    after: datetime,
    before: datetime,
    database_operations: DatabaseOperations,
):
    logger.info(f"Loading activity data between {after} and {before} from strava.")
    strava_client = get_strava_client(session_id=session_id)
    activities = [
        act
        for act in strava_client.get_activities(after=after, before=before, limit=100)
    ]
    database_operations.insert_activities(
        user=user,
        activities=activities,
    )
