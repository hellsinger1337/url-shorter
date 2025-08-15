from datetime import datetime

from pydantic import AnyUrl, BaseModel, Field


class ShortenRequest(BaseModel):
    url: AnyUrl = Field(..., description="Оригинальный URL")


class ShortenResponse(BaseModel):
    code: str
    short_url: AnyUrl


class StatsResponse(BaseModel):
    code: str
    original_url: AnyUrl
    clicks: int
    created_at: datetime
