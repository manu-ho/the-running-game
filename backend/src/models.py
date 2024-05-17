from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Interval,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, registry


# Overwrite default constructor with this method to ignore additional kwargs in constructors
def lenient_constructor(self, **kwargs):
    cls_ = type(self)
    for k in kwargs:
        if not hasattr(cls_, k):
            continue
        setattr(self, k, kwargs[k])


default_registry = registry(constructor=lenient_constructor)


class Base(DeclarativeBase):
    registry = default_registry


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    session_id = Column(String)
    access_token = Column(String)
    expires_at = Column(Integer)

    refresh_token_id = mapped_column(ForeignKey("refresh_token.id"))
    refresh_token = relationship("RefreshToken", back_populates="sessions")

    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="sessions")


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String)

    sessions = relationship("Session", back_populates="refresh_token")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    athlete_id = Column(BigInteger)

    firstname = Column(String)
    lastname = Column(String)
    sex = Column(String)
    city = Column(String)
    country = Column(String)
    profile_medium = Column(String)

    sessions = relationship("Session", back_populates="user")
    activities = relationship("Activity", back_populates="user")


class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, autoincrement=True)

    activity_id = Column(BigInteger)

    name = Column(String)
    distance = Column(Float)
    moving_time = Column(Interval)
    start_date = Column(DateTime)
    description = Column(String)
    location_city = Column(String)

    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="activities")
