from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.db.crud import (create_custom_slug, create_slug, get_stats_from_slug,
                          get_url_from_slug)
from core.db.db import engine, get_db
from core.db.exceptions import (CustomSlugError, NotFoundSlugError,
                                NotFoundStatisticsError)
from core.schemas import CustomSlug, SlugInfo, UrlBase


@asynccontextmanager
async def lifespan(my_app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/create_slug")
async def create_slug_url(
    url: UrlBase,
    session: Annotated[AsyncSession, Depends(get_db)],
) -> str:
    try:
        slug = await create_slug(
            url=url.url,
            session=session,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return slug


@app.post("/create_custom_slug")
async def create_custom_slug_url(
    CustomSlug: CustomSlug,
    session: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    try:
        custom_slug = await create_custom_slug(
            url=CustomSlug.url,
            slug=CustomSlug.slug,
            session=session,
        )
    except CustomSlugError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return {"msg": f"Slug {custom_slug} successfully created!"}


@app.get("/stats", response_model=SlugInfo)
async def get_stats(
    slug: str,
    session: AsyncSession = Depends(get_db),
) -> SlugInfo:
    try:
        stats = await get_stats_from_slug(
            slug=slug,
            session=session,
        )
    except NotFoundStatisticsError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return stats


@app.get("/{slug}")
async def redirect_to_slug(
    slug: str,
    session: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    try:
        url = await get_url_from_slug(
            slug=slug,
            session=session,
        )
    except NotFoundSlugError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
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
