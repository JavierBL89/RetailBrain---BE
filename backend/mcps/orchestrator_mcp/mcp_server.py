from fastmcp import FastMCP
import os


SERVICE_TOKEN = os.getenv("MCP_SERVICE_TOKEN", "change-me")


mcp = FastMCP("orchestrator")

# AUTH

@mcp.tool
def require_auth(request, next):
    """
    Simple service-to-service authentication middleware.
    Ensures only requests with a valid X-Service-Token header can access the MCP.
    """

    token=None
    if(hasattr(request, "headers")):
        token = request.headers.get("X-Service-Token")
    elif isinstance(request, dict):
        token = request.get("headers", {}).get("X-Service-Token")

    if token != SERVICE_TOKEN:
        # Return an MCP-compliant error
        raise PermissionError("Unauthorized: Invalid X-Service-Token header")
    
    return next(request)

# ------------------------------------------------------
# TOOLS / ENDPOINTS
# ------------------------------------------------------
@mcp.tool
def health() -> str:
    """
    Health check endpoint.
    Returns 'OK' if the service is running.
    """
    return "OK"

@mcp.tool
def echo(message: str) -> str:
    """Simple echo tool for testing connectivity."""
    return f"Server received: {message}"


# ------------------------------------------------------
# RUN SERVER (STREAMABLE HTTP MODE)
# ------------------------------------------------------
if __name__ == "__main__":
    # Expose the MCP server as a Streamable HTTP endpoint
    # Default port: 8000, endpoint: /mcp
    print("FastMCP Orchestrator started on port 8000")
    # Get the FastAPI app from FastMCP
    # mcp.run(transport="http", host="0.0.0.0", port=8000)
    mcp.run(transport="http", host="127.0.0.1", port=8000)
