from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl
from .mixins import UrlNormalizationMixin, SlugValidationMixin


class SlugBase(BaseModel, SlugValidationMixin):
    slug: str = Field(min_length=3, max_length=32)


class UrlBase(BaseModel, UrlNormalizationMixin):
    url: HttpUrl


class CustomSlug(BaseModel, SlugValidationMixin, UrlNormalizationMixin):
    slug: str = Field(min_length=3, max_length=32)
    url: HttpUrl


class SlugInfo(BaseModel):
    url: str
    slug: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True
