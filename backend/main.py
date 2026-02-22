from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager
from config.config import settings

from database import setup_database

from routers import task, auth, oauth, profile

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
