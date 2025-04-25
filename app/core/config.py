import os
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()

# Facebook API configuration
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_API_VERSION = os.getenv("FACEBOOK_API_VERSION", "2.12")

# API settings
API_V1_STR = "/api/v1"
PROJECT_NAME = "Facebook Page Manager API"

# Configure logger
logger.add("logs/facebook_api.log", rotation="10 MB", level="INFO")

# Validate required environment variables
if not FACEBOOK_ACCESS_TOKEN:
    logger.error("FACEBOOK_ACCESS_TOKEN environment variable is not set")
    raise ValueError("FACEBOOK_ACCESS_TOKEN environment variable is not set")
