from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.db.crud import add_slug_db, url_from_slug
from core.db.db import engine, get_db
from core.utils import create_slug, validated_url


@asynccontextmanager
async def lifespan(my_app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/shortlink")
async def create_slug_url(
    url: str = Query(...),
    session: AsyncSession = Depends(get_db),
) -> str:
    try:
        validated_url(url=url)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    slug = create_slug()

    await add_slug_db(
        url=url,
        slug=slug,
        session=session,
    )

    return slug


@app.get("/{slug}")
async def redirect_to_slug(
    slug: str,
    session: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    url = await url_from_slug(
        slug=slug,
        session=session,
    )
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slug doesn't exist",
        )

    return RedirectResponse(
        url=url,
        status_code=302,
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
