from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core import settings
from core.db.db import engine


@asynccontextmanager
async def lifespan(my_app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
