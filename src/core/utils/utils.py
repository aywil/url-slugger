import secrets
import string

import validators

GENERATE_SHORTLINK = string.ascii_letters + string.digits


def create_slug() -> str:
    slug = ""
    for _ in range(6):
        slug += secrets.choice(GENERATE_SHORTLINK)
    return slug
