import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.database import init_db

settings = get_settings()
setup_logging(settings.ENVIRONMENT)

from app.api import auth, tools, settings as settings_api, users, audit, stats

app = FastAPI(title="Apps Startpage", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tools.router, prefix="/api", tags=["tools"])
app.include_router(settings_api.router, prefix="/api", tags=["settings"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(audit.router, prefix="/api", tags=["audit"])
app.include_router(stats.router, prefix="/api", tags=["stats"])


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield


app.router.lifespan_context = lifespan


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
