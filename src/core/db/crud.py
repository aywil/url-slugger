import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ShortLink
from core.schemas import UrlInfo

from .exceptions import NotFoundSlugError, NotFoundStatisticsError
from .utils import GENERATE_SHORTLINK, get_shortlink_table_from_slug, validated_url


async def create_slug(
    url: str,
    session: AsyncSession,
) -> str:
    try:
        safe_url = validated_url(url=url)
    except ValueError as e:
        raise e

    slug = ""
    for _ in range(6):
        slug += secrets.choice(GENERATE_SHORTLINK)

    shortlink = ShortLink(
        slug=slug,
        url=safe_url,
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
    return result.url


async def get_stats_from_slug(
    slug: str,
    session: AsyncSession,
) -> UrlInfo | None:
    stats = await get_shortlink_table_from_slug(
        slug=slug,
        session=session,
    )
    if not stats:
        raise NotFoundStatisticsError(f"Statistics about {slug} doesn't exist")
    return stats


async def count_clicks_to_slug():
    pass
