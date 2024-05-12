import logging
from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session
from src import models

logger = logging.getLogger(__name__)


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
    ) -> models.Session:
        refresh_t = models.RefreshToken(refresh_token=refresh_token)
        session = models.Session(
            session_id=session_id,
            access_token=access_token,
            expires_at=expires_at,
            refresh_token=refresh_t,
        )
        with self.session_factory() as db:
            db.add(refresh_t)
            db.add(session)
            db.commit()
            db.refresh(session)
            return session

    def get_session_token(self, sesstion_id: str) -> models.Session:
        with self.session_factory() as db:
            return (
                db.query(models.Session)
                .filter(models.Session.session_id == sesstion_id)
                .first()
            )

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
