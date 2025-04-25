from fastapi import Request, status
from fastapi.responses import JSONResponse
from facebook import GraphAPIError
from loguru import logger

class FacebookAPIException(Exception):
    """Custom exception for Facebook API errors"""
    def __init__(self, status_code: int, message: str, details: str = None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(self.message)

async def facebook_exception_handler(request: Request, exc: GraphAPIError):
    """Handler for Facebook GraphAPIError exceptions"""
    status_code = getattr(exc, "code", 500)
    message = str(exc)
    
    logger.error(f"Facebook API error: {message}")
    
    return JSONResponse(
        status_code=status_code,
        content={"error": True, "message": "Facebook API error", "details": message}
    )

async def facebook_api_exception_handler(request: Request, exc: FacebookAPIException):
    """Handler for custom FacebookAPIException"""
    logger.error(f"Facebook API exception: {exc.message}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "details": exc.details
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handler for general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error",
            "details": str(exc)
        }
    )
