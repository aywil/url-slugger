import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ShortLink
from core.schemas import SlugInfo

from .exceptions import CustomSlugError, NotFoundSlugError, NotFoundStatisticsError
from .utils import (
    GENERATE_SHORTLINK,
    get_shortlink_table_from_slug,
)


async def create_slug(
    url: str,
    session: AsyncSession,
) -> str:
    slug = ""
    for _ in range(6):
        slug += secrets.choice(GENERATE_SHORTLINK)

    shortlink = ShortLink(
        slug=slug,
        url=str(url),
    )
    session.add(shortlink)
    await session.commit()

    return slug


async def create_custom_slug(
    url: str,
    slug: str,
    session: AsyncSession,
) -> str:
    result = await get_shortlink_table_from_slug(
        slug=str(slug),
        session=session,
    )
    if result:
        raise CustomSlugError(f"Slug: {slug} is busy")

    shortlink = ShortLink(
        slug=str(slug),
        url=str(url),
    )
    session.add(shortlink)
    await session.commit()

    return slug


async def get_url_from_slug(
    slug: str,
    session: AsyncSession,
) -> str:

    result = await get_shortlink_table_from_slug(
        slug=slug,
        session=session,
    )
    if not result:
        raise NotFoundSlugError(f"Slug {slug} doesn't exist")
    result.clicks += 1
    await session.commit()
    return result.url


async def get_stats_from_slug(
    slug: str,
    session: AsyncSession,
) -> SlugInfo | None:
    stats = await get_shortlink_table_from_slug(
        slug=slug,
        session=session,
    )
    if not stats:
        raise NotFoundStatisticsError(f"Statistics about {slug} doesn't exist")
    return stats
