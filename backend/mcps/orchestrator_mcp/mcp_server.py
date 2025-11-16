from fastmcp import FastMCP
import sys, os

import logging
import json
from llama_client import query_llama_api


logging.basicConfig(level=logging.INFO)

SERVICE_TOKEN = os.getenv("MCP_SERVICE_TOKEN", "change-me")

mcp = FastMCP("orchestrator")


# ------------------------------------------------------
# HEALTH TOOLS / ENDPOINTS
# ------------------------------------------------------
@mcp.tool
def insert_product(product: dict) -> str:
    """
    Insert a new product into the inventory system.
    Currently logs the request for testing purposes.
    """

    # Log the request
    logging.info("=" * 20)
    logging.info("📦 INSERT PRODUCT REQUEST")
    logging.info("=" * 20)
    logging.info(json.dumps(product, indent=2))
    logging.info("=" * 20)
     # Return success response
    return json.dumps({
        "status": "success",
        "message": f"Product '{product.get('name')}' logged successfully",
        "product": product
    }, indent=2)


@mcp.tool
def semantic_products_search(user_query: dict):
    """
    Perform a semantic search for products based on user query.
    """

    # Call LLaMA API to extract intent/entities
    query_llama_api(user_query['query'])
    
    # Save last message to session for state persistence
    return {"result": "hello"}


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
# HEALTH TOOLS / ENDPOINTS
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
if __name__ == "__main__":
    # Expose the MCP server as a Streamable HTTP endpoint
    print("FastMCP Orchestrator started on port 8000")

    mcp.run(transport="http", host="0.0.0.0", port=8000)
    #mcp.run(transport="http", host="127.0.0.1", port=8000) # Use this for local 