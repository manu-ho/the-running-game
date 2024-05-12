import logging
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from src import models

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, connection_string: str) -> None:
        self._engine = create_engine(connection_string)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        # TODO use alembic for migration
        # models.Base.metadata.drop_all(self._engine)  # FIXME: remove this line!
        models.Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Iterator[Session]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
