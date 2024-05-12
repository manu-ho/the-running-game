from datetime import datetime
from pydantic import BaseModel


class LoginUrl(BaseModel):
    authorization_url: str


class RefreshTokenResponse(BaseModel):
    success: bool
    expiration_date: datetime
