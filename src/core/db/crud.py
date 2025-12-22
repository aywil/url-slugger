from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ShortLink


async def add_slug_db(
    url: str,
    slug: str,
    session: AsyncSession,
):

    shortlink = ShortLink(
        slug=slug,
        url=url,
    )
    session.add(shortlink)
    await session.commit()


async def url_from_slug(
    slug: str,
    session: AsyncSession,
):
    result = await session.execute(select(ShortLink).where(ShortLink.slug == slug))
    shortlink = result.scalar_one_or_none()

    if not shortlink:
        return None

    shortlink.clicks += 1
    await session.commit()

    return shortlink.url
