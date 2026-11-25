from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (register models with SQLModel metadata)
from app.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Bookmark Vault", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
