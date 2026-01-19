from fastapi import FastAPI
import uvicorn

from database import setup_database

from contextlib import asynccontextmanager

from routers import getHandlers, postHandlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(getHandlers.router)
app.include_router(postHandlers.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
