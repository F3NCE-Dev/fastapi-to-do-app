from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager
from config.config import settings

from database import setup_database
from routers import AuthorizationRouter, TaskHandlersRouter, ProfileEditRouter, OAuthAuthorizationRouter

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

app.include_router(TaskHandlersRouter.router)
app.include_router(AuthorizationRouter.router)
app.include_router(OAuthAuthorizationRouter.router)
app.include_router(ProfileEditRouter.router)

app.mount("/media", StaticFiles(directory=settings.MEDIA_DIR, check_dir=False), name="media")
app.mount("/default_media", StaticFiles(directory=settings.DEFAULT_USER_PROFILE_PIC_DIR, check_dir=False), name="default_media")
