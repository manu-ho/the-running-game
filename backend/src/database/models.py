from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Interval,
    String,
    Tuple,
    TypeDecorator,
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


class LatLngModelType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, _):
        if isinstance(value, list) or isinstance(value, tuple):
            return f"{value[0]},{value[1]}"
        raise ValueError(
            f"Error mapping value of type {type(value)} to LatLng in database."
        )

    def process_result_value(self, value, _):
        return tuple([float(val) for val in value.split(",")])


class TimeStreamDataModelType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, _):
        if isinstance(value, list):
            return ",".join(str(item) for item in value)
        raise ValueError(
            f"Error mapping value of type {type(value)} to TimeStreamData in database."
        )

    def process_result_value(self, value, _):
        if value is None:
            return value
        return [float(val) for val in value.split(",")]


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

    id = mapped_column(Integer, primary_key=True, autoincrement=True)

    activity_id = Column(BigInteger)

    name = Column(String)
    distance = Column(Float)
    moving_time = Column(Interval)
    total_elevation_gain = Column(Float)
    start_date = Column(DateTime)
    start_latlng = Column(LatLngModelType)
    end_latlng = Column(LatLngModelType)
    has_heartrate = Column(Boolean)
    description = Column(String)
    location_city = Column(String)

    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="activities")

    time_streams = relationship("TimeStream", back_populates="activity")
    latlng_streams = relationship("LatLngStream", back_populates="activity")


class TimeStream(Base):
    __tablename__ = "time_stream"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)

    original_size = Column(BigInteger)
    series_type = Column(String)

    data = Column(TimeStreamDataModelType)

    activity_id = mapped_column(ForeignKey("activity.id"))
    activity = relationship("Activity", back_populates="time_streams")


class LatLngStream(Base):
    __tablename__ = "latlng_stream"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)

    original_size = Column(BigInteger)
    series_type = Column(String)

    # data = Column(LatLngStreamDataModelType)  # FIXME define the data type

    activity_id = mapped_column(ForeignKey("activity.id"))
    activity = relationship("Activity", back_populates="latlng_streams")


# class Stream:
#     id = Column(Integer, primary_key=True, autoincrement=True)

#     original_size = Column(BigInteger)
#     series_type = Column(String)


# class TimeStream(Base, Stream):
#     __tablename__ = "time_stream"

#     data = Column(TimeStreamDataModelType)

#     activity_id = mapped_column(ForeignKey("activity.id"))
#     activity = relationship("Activity", back_populates="time_streams")


# class LatLngStream(Base, Stream):
#     __tablename__ = "latlng_stream"

#     # data = Column(LatLngStreamDataModelType)  # FIXME define the data type

#     activity_id = mapped_column(ForeignKey("activity.id"))
#     activity = relationship("Activity", back_populates="latlng_streams")
