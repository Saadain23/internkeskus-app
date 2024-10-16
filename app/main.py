# app/main.py

from fastapi import FastAPI
from app.api.endpoints import auth, students, recruiters, profiles
from app.core.config import settings
from app.middleware.error_handlers import add_exception_handlers
from app.middleware.logging import LoggingMiddleware
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.db.init_db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    await init_db()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(students.router, prefix="/api/students", tags=["students"])
app.include_router(recruiters.router, prefix="/api/recruiters", tags=["recruiters"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["profiles"])

# Add middleware
app.add_middleware(LoggingMiddleware)

# Add exception handlers
add_exception_handlers(app)
