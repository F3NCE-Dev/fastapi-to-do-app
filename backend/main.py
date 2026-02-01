from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

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
    allow_origins=[settings.FRONTEND_URL, "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(TaskHandlersRouter.router)
app.include_router(AuthorizationRouter.router)
app.include_router(OAuthAuthorizationRouter.router)
app.include_router(ProfileEditRouter.router)

app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/default_media", StaticFiles(directory="default_media"), name="default_media")

if __name__ == "__main__":
    uvicorn.run("main:app")
