import re
from pydantic import field_validator
import validators


class UrlNormalizationMixin:
    @field_validator("url", mode="before")
    @classmethod
    def normalize_url_before_validation(cls, v: str) -> str:
        if isinstance(v, str):
            if not validators.url(v):
                if validators.url(f"https://{v}"):
                    return f"https://{v}"
        return v


class SlugValidationMixin:
    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9\-]+$", v):
            raise ValueError("Slug can only contain letters, numbers, and hyphens")

        if v.startswith("-") or v.endswith("-"):
            raise ValueError("Slug cannot start or end with a hyphen")

        if "--" in v:
            raise ValueError("Slug cannot contain consecutive hyphens")

        return v
