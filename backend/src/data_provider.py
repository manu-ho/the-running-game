import logging
from datetime import datetime

import pytz
import stravalib
from dependency_injector.wiring import Provide, inject
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError
from src import schemas
from src.database import models
from src.database.database_operations import DatabaseOperations
from src.dependency_container import DependencyContainer
from src.exceptions import DatabaseException

logger = logging.getLogger(__name__)


class DataProvider:

    @inject
    def __init__(
        self,
        session_id: str,
        database_operations: DatabaseOperations = Provide[
            DependencyContainer.database_operations
        ],
    ):
        self.session_id: str = session_id
        self.database_operations: DatabaseOperations = database_operations
        self._session: models.Session = None

    @property
    def session(self) -> models.Session:
        if self._session is None:
            self._session = self._get_session()
        return self._session

    def _get_session(self) -> models.Session:
        try:
            return self.database_operations.get_session(session_id=self.session_id)
        except SQLAlchemyError as e:
            raise DatabaseException(
                error_code=status.HTTP_401_UNAUTHORIZED,
                message=f"Could not get session from database. {e}",
            )

    def get_strava_client(self) -> stravalib.Client:
        client_session = self.session
        token = client_session.access_token
        if token:
            return stravalib.Client(access_token=token)
        raise ValueError(f"Could not get session from database.")

    def get_user(self) -> models.User:
        try:
            return self.database_operations.get_user(session_id=self.session_id)
        except SQLAlchemyError as e:
            raise DatabaseException(
                error_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                message=f"Could not get user from database. {e}",
            )

    def get_activities(
        self,
        after: datetime,
        before: datetime,
        limit: int = 100,
        detailed: bool = False,
    ) -> list[schemas.Activity]:
        try:
            user = self.database_operations.get_user(session_id=self.session_id)
            if user is None:
                raise DatabaseException(
                    error_code=status.HTTP_404_NOT_FOUND,
                    message=f"Could not get user for session {self.session_id}",
                )
            self._pull_activities_from_strava_into_database(
                user=user,
                after=after,
                before=before,
                limit=limit,
            )
            activities = self.database_operations.get_activities(
                user=user, after=after, before=before, detailed=detailed
            )
        except SQLAlchemyError as e:
            raise DatabaseException(
                error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Could not update and get activities in database. {e}",
            )
        activities = [schemas.Activity.from_orm(act) for act in activities]
        return activities

    def _pull_activities_from_strava_into_database(
        self,
        user: models.User,
        after: datetime,
        before: datetime,
        limit: int = 100,
    ) -> None:
        after = after.replace(tzinfo=pytz.UTC)
        before = before.replace(tzinfo=pytz.UTC)
        pre_loaded_activity_timerange = (
            self.database_operations.get_activity_timerange_present(user=user)
        )
        logger.info(
            f"Found activity data between {pre_loaded_activity_timerange[0]} and "
            f"{pre_loaded_activity_timerange[1]} in database."
        )
        if (
            pre_loaded_activity_timerange[0] is None
            or pre_loaded_activity_timerange[1] is None
        ):
            self._ingest_activities_from_strava(
                user=user,
                after=after,
                before=before,
                limit=limit,
            )
            return
        if after < pre_loaded_activity_timerange[0]:
            self._ingest_activities_from_strava(
                user=user,
                after=after,
                before=pre_loaded_activity_timerange[0],
                limit=limit,
            )
        if pre_loaded_activity_timerange[1] < before:
            self._ingest_activities_from_strava(
                user=user,
                after=pre_loaded_activity_timerange[1],
                before=before,
                limit=limit,
            )

    def _ingest_activities_from_strava(
        self,
        user: models.User,
        after: datetime,
        before: datetime,
        limit: int = 100,
    ):
        logger.info(f"Loading activity data between {after} and {before} from strava.")
        strava_client = self.get_strava_client()
        activities = [
            act
            for act in strava_client.get_activities(
                after=after, before=before, limit=limit
            )
        ]
        streams_of_all_activities = [
            strava_client.get_activity_streams(act.id) for act in activities
        ]
        self.database_operations.insert_activities(
            user=user,
            activities=activities,
            streams_of_all_activities=streams_of_all_activities,
        )
