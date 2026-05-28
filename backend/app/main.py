from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager
from app.config.config import settings

from app.routers import auth, oauth, profile
from app.database import setup_database

from app.routers import task

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task.router)
app.include_router(auth.router)
app.include_router(oauth.router)
app.include_router(profile.router)

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR, check_dir=False), name="static")
