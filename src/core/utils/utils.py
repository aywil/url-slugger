import secrets
import string

import validators

GENERATE_SHORTLINK = string.ascii_letters + string.digits


def create_slug() -> str:
    slug = ""
    for _ in range(6):
        slug += secrets.choice(GENERATE_SHORTLINK)
    return slug


def validated_url(url: str) -> str:
    if not validators.url(url):
        if validators.url(f"https://{url}"):
            url = f"https://{url}"
        else:
            raise ValueError("Invalid URL")
    return url
