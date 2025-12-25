from datetime import datetime

from pydantic import BaseModel


class UrlInfo(BaseModel):
    url: str
    slug: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True
