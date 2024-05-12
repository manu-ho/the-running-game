from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column


class Base(DeclarativeBase):
    pass


class Session(Base):
    __tablename__ = "session"

    id = mapped_column(Integer, primary_key=True)

    session_id = Column(String)

    access_token = Column(String)
    expires_at = Column(Integer)
    refresh_token_id = mapped_column(ForeignKey("refresh_token.id"))
    refresh_token = relationship("RefreshToken", back_populates="sessions")


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = mapped_column(Integer, primary_key=True)

    refresh_token = mapped_column(String)
    sessions = relationship("Session", back_populates="refresh_token")
