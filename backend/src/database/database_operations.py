import logging
from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable, List, Mapping, Tuple

import pytz
import stravalib.model
from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session, joinedload, noload
from src.database import models

logger = logging.getLogger(__name__)

_stream_type_mapping = {
    "time": models.TimeStream,
    "latlng": models.LatLngStream,
}


class DatabaseOperations:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def add_session_token(
        self,
        session_id: str,
        access_token: str,
        expires_at: int,
        refresh_token: str,
        athlete: stravalib.model.Athlete,
    ) -> models.Session:
        user_db = self.add_user_if_not_exists(athlete=athlete)

        refresh_t = models.RefreshToken(token=refresh_token)
        session = models.Session(
            session_id=session_id,
            access_token=access_token,
            expires_at=expires_at,
            refresh_token=refresh_t,
            user=user_db,
        )
        with self.session_factory() as db:
            db.add(refresh_t)
            db.add(session)
            db.commit()
            db.refresh(session)
            return session

    def add_user_if_not_exists(self, athlete: stravalib.model.Athlete) -> models.User:
        with self.session_factory() as db:
            existing_user = (
                db.query(models.User).filter_by(athlete_id=athlete.id).first()
            )
            if existing_user:
                user_db = existing_user
            else:
                user_db = models.User(
                    **athlete.dict(
                        exclude_unset=True,
                        exclude_none=True,
                        exclude={"id"},
                    ),
                    athlete_id=athlete.id,
                )
                db.add(user_db)
                db.commit()
                db.refresh(user_db)
        return user_db

    def get_session(self, session_id: str) -> models.Session:
        with self.session_factory() as db:
            return (
                db.query(models.Session)
                .filter(models.Session.session_id == session_id)
                .first()
            )

    def get_user(self, session_id: Session) -> models.User:
        with self.session_factory() as db:
            return (
                db.query(models.User)
                .options(joinedload(models.User.sessions))
                .filter(models.Session.session_id == session_id)
                .first()
            )

    def insert_activities(
        self,
        user: models.User,
        activities: List[stravalib.model.Activity],
        streams_of_all_activities: List[Mapping[str, stravalib.model.Stream]],
    ):
        activities_db = []
        streams_db = []
        for activity, activity_streams in zip(activities, streams_of_all_activities):
            activity_db = models.Activity(
                **activity.dict(exclude_unset=True, exclude_none=True, exclude={"id"}),
                activity_id=activity.id,
                user_id=user.id,
            )
            activities_db.append(activity_db)
            for stream_key, stream in activity_streams.items():
                stream_type = _stream_type_mapping.get(stream_key, None)
                if stream_type is None:
                    logger.warning(
                        f"Could not map {stream_key} to a stream type. Skipping stream."
                    )
                    continue
                streams_db.append(
                    stream_type(
                        **stream.dict(
                            exclude_unset=True, exclude_none=True, exclude={"id"}
                        ),
                        activity_id=activity_db.id,  # FIXME the FK is always null
                        activity=activity_db,
                    )
                )

        with self.session_factory() as db:
            db.bulk_save_objects(activities_db, update_changed_only=False)
            db.commit()
            db.bulk_save_objects(streams_db, update_changed_only=False)
            db.commit()

    def get_activity_timerange_present(
        self, user: models.User
    ) -> Tuple[datetime, datetime]:
        with self.session_factory() as db:
            from_date = (
                db.query(func.min(models.Activity.start_date))
                .filter(models.Activity.user_id == user.id)
                .scalar()
            )
            to_date = (
                db.query(func.max(models.Activity.start_date))
                .filter(models.Activity.user_id == user.id)
                .scalar()
            )
        from_date = (
            from_date.replace(tzinfo=pytz.UTC) if from_date is not None else None
        )
        to_date = to_date.replace(tzinfo=pytz.UTC) if to_date is not None else None
        return from_date, to_date

    def get_activities(
        self,
        user: models.User,
        before: datetime,
        after: datetime,
        detailed: bool = False,
    ) -> List[models.Activity]:
        with self.session_factory() as db:
            stmt = (
                select(models.Activity).options(
                    noload(models.Activity.time_streams),
                    noload(models.Activity.latlng_streams),
                )
                if not detailed
                else select(models.Activity).options(
                    joinedload(models.Activity.time_streams),
                    joinedload(models.Activity.latlng_streams),
                )
            )
            stmt = stmt.where(
                and_(
                    models.Activity.user_id == user.id,
                    models.Activity.start_date > after,
                    models.Activity.start_date < before,
                )
            )
            return db.execute(stmt).unique().scalars().all()

    # def get_item(self, item_id: int) -> models.Item:
    #     with self.session_factory() as session:
    #         return session.query(models.Item).filter(models.Item.id == item_id).first()

    # def get_items(
    #     self, skip: int = 0, limit: int = 100, state_filter: ItemState | None = None
    # ) -> List[models.Item]:
    #     with self.session_factory() as session:
    #         if state_filter is not None:
    #             return (
    #                 session.query(models.Item)
    #                 .where(models.Item.state == state_filter)
    #                 .order_by(models.Item.number_label)
    #                 .offset(skip)
    #                 .limit(limit)
    #                 .all()
    #             )
    #         return (
    #             session.query(models.Item)
    #             .order_by(models.Item.number_label)
    #             .offset(skip)
    #             .limit(limit)
    #             .all()
    #         )

    # def _create_item(self, database_item: models.Item) -> models.Item:
    #     database_item.approval_id = str(uuid4())
    #     with self.session_factory() as session:
    #         session.add(database_item)
    #         session.commit()
    #         session.refresh(database_item)
    #         return database_item

    # def create_item(self, item: schemas.ItemCreate) -> models.Item:
    #     database_item = models.Item(**item.model_dump())
    #     database_item.state = ItemState.NEW
    #     return self._create_item(database_item)

    # def create_manual_item(self, item: schemas.ItemManualCreate) -> models.Item:
    #     database_item = models.Item(**item.model_dump())
    #     database_item.state = ItemState.ACTIVE
    #     database_item.pick_up_code = database_item.number_label
    #     return self._create_item(database_item)

    # def update_item(
    #     self, item_id: int, item_update: schemas.ItemUpdate | models.Item
    # ) -> models.Item:
    #     database_item = self.get_item(item_id=item_id)
    #     with self.session_factory() as session:
    #         database_item = (
    #             session.query(models.Item).filter(models.Item.id == item_id).first()
    #         )
    #         if database_item is None:
    #             raise ValueError(f"Item with {item_id=} not found.")
    #         if (
    #             item_update.price is not None
    #             and int(database_item.price) != int(item_update.price)
    #             and database_item.state not in [ItemState.NEW, ItemState.APPROVED]
    #         ):
    #             # Only allow price updates before the item is ACTIVE!!!
    #             raise PermissionError(
    #                 f"Price update not allowed in state {database_item.state}."
    #             )
    #         # if database_item.state in [
    #         #     ItemState.PICKED_UP_CASH,
    #         #     ItemState.PICKED_UP_ITEM,
    #         # ]:
    #         #     raise PermissionError(f"Item has final state of {database_item.state}.")
    #         item_data = item_update.model_dump(exclude_unset=True)
    #         for key, value in item_data.items():
    #             setattr(database_item, key, value)
    #         session.add(database_item)
    #         session.commit()
    #         session.refresh(database_item)
    #         return database_item

    # def get_item_from_approval_id(self, approval_id: str) -> models.Item:
    #     with self.session_factory() as session:
    #         return (
    #             session.query(models.Item)
    #             .filter(models.Item.approval_id == approval_id)
    #             .first()
    #         )

    # def get_number_labels_in_use(self) -> List[int]:
    #     with self.session_factory() as session:
    #         return [
    #             number_label
    #             for (number_label,) in session.query(models.Item.number_label)
    #             .distinct()
    #             .all()
    #             if number_label is not None
    #         ]
