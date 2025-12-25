import string

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ShortLink

GENERATE_SHORTLINK = string.ascii_letters + string.digits


async def get_shortlink_table_from_slug(slug: str, session: AsyncSession):
    stmt = await session.execute(select(ShortLink).where(ShortLink.slug == slug))
    result = stmt.scalar_one_or_none()
    return result
