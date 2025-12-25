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
