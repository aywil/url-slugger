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
