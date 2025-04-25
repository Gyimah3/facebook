from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from facebook import GraphAPIError

from app.api.endpoints import facebook
from app.core.config import API_V1_STR, PROJECT_NAME
from app.core.error_handlers import (
    facebook_exception_handler,
    facebook_api_exception_handler,
    FacebookAPIException,
    general_exception_handler
)

# Create FastAPI app
app = FastAPI(
    title=PROJECT_NAME,
    description="API for managing Facebook page data",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(GraphAPIError, facebook_exception_handler)
app.add_exception_handler(FacebookAPIException, facebook_api_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include API routers
app.include_router(facebook.router, prefix=f"{API_V1_STR}/facebook", tags=["facebook"])

@app.get("/")
async def root():
    """Root endpoint to check if API is running"""
    return {
        "status": "online",
        "message": "Facebook Page Manager API is running",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
