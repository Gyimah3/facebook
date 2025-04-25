import os
import sys
from loguru import logger
from fastapi_mcp import FastApiMCP
# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import FastAPI app
from app.main import app
# mcp = FastApiMCP(
#     app,

#     # Optional parameters
#     name="My API MCP",
#     description="My API description",
#     base_url="http://localhost:8000",
# )

# # Mount the MCP server directly to your FastAPI app
# mcp.mount()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
# add_mcp_server(app, mount_path="/mcp", name="My API MCP")
# if __name__ == "__main__":
#     import uvicorn
#     logger.info("Starting Facebook Page Manager API server")
#     uvicorn.run(app, host="0.0.0.0", port=8000)
