from datetime import datetime
from typing import Any, List
from pydantic import BaseModel


class LoginUrl(BaseModel):
    authorization_url: str


class RefreshTokenResponse(BaseModel):
    success: bool
    expiration_date: datetime


class Athlete(BaseModel):
    class Config:
        orm_mode = True

    id: int
    firstname: str
    lastname: str
    sex: str
    city: str
    country: str
    profile_medium: str
    sessions: List[Any]
