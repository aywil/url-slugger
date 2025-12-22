from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core import settings

engine = create_async_engine(
    url=str(settings.db.url),
    echo=True,
)

session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db():
    async with session() as db_session:
        yield db_session
        await db_session.close()
