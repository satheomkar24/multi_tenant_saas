from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.core.errors import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler
)
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.middlewares.tenantMiddleware import TenantMiddleware
from app.auth.routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    print("✅ MongoDB connected")
    
    # You can start background tasks, load caches, etc.
    
    yield  # FastAPI runs here
    
    # Shutdown
    await close_mongo_connection()
    print("🛑 MongoDB disconnected")



app = FastAPI(
    title="Multi-Tenant SaaS Backend",
    description="FastAPI + MongoDB + Motor + Multi-Tenant Example",
    version="0.1.0"
)

print(settings.CORS_ORIGINS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    unhandled_exception_handler
)

app.add_middleware(TenantMiddleware)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}


