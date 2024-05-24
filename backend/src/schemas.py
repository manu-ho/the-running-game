from datetime import datetime, timedelta
from typing import Optional, Tuple
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


class Activity(BaseModel):
    class Config:
        orm_mode = True

    activity_id: int
    name: str
    distance: float
    moving_time: timedelta
    total_elevation_gain: float
    start_date: datetime
    start_latlng: Tuple[float, float]
    end_latlng: Tuple[float, float]
    has_heartrate: bool
    description: Optional[str]
    location_city: Optional[str]
