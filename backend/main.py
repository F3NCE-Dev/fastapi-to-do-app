from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers import authorizationRouter
from database import setup_database

from contextlib import asynccontextmanager

from routers import getHandlers, postHandlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield

app = FastAPI(lifespan=lifespan, title="To-Do-API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(getHandlers.router)
app.include_router(postHandlers.router)
app.include_router(authorizationRouter.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
