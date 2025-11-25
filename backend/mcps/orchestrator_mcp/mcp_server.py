from fastmcp import FastMCP
import sys, os
from pathlib import Path
import logging
import json


from llm.gpt_client import query_gpt_api
#from mcps.product_v_search.main import process_search
#from mcps.product_v_search.main import upsert_products
from mcps.db_analytics.inventory_manager import insert_new_product_sql

logging.basicConfig(level=logging.INFO)

SERVICE_TOKEN = os.getenv("MCP_SERVICE_TOKEN", "change-me")

mcp = FastMCP("orchestrator")



# ------------------------------------------------------
# Tools
# ------------------------------------------------------
@mcp.tool
def route_request( action: str,  
    product: dict | None = None,
    user_query: dict | None = None,
    conversation_id: str | None = None,):
    """
    Route incoming requests to appropriate handlers based on tool_name.
    """   

    if action == "insert_product":
        # Insert new product into SQL database
        # try:
        #    new_variants_list = insert_new_product_sql(product or {})
        #except Exception as e:
        ##    return {"error": f"Failed to insert product into SQL db: {str(e)}"}
        ##return {"Products added to SQL db ": new_variants_list}
        
        return "Route request tool reached for insert_product"
        #return upsert_product(product or {})  ## Product vector db insertion 
    
    elif action == "semantic_products_search":
        #return vector_search(conversation_id, user_query or {})
        return "Route request tool reached for semantic_products_search"
    
    elif action == "health":
        return health()
    
    elif action == "echo":

        message = action.get("message", "")
        return echo(message)
    else:
        return {"error": f"Unknown action: {action}"}


# ------------------------------------------------------
# HEALTH TOOLS / ENDPOINTS
# ------------------------------------------------------
def upsert_product(product: dict) -> str:
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
    
    ###### Use stdio transport for Claude Desktop ######
    #print("FastMCP Orchestrator started with stdio transport", file=sys.stderr)
    #mcp.run(transport="stdio")