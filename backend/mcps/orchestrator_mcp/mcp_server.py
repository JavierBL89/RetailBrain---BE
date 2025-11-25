from fastmcp import FastMCP
import sys, os
from pathlib import Path
import logging
import json


from llm.gpt_client import query_gpt_api
#from mcps.product_v_search.main import process_search
#from mcps.product_v_search.main import upsert_products
from mcps.inventory_management.inventory_manager import insert_new_product_sql, fetch_all_products_variants

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
    Route incoming requests to appropriate handlers based on action name.
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
        return process_vector_search(conversation_id, user_query or {})
    
    elif action == "fetch_products":
        return fetch_all_products_variants()
    
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



chat_memory={} # Dict[str, List[Dict[str, str]]]

def process_vector_search(conversation_id:str, user_query: dict):
    """
    Perform a semantic search for products based on user query.
    """
    if conversation_id not in chat_memory:
        chat_memory[conversation_id] = []


    current_user_text = user_query.get('query', '')
    # Add user query to conversation history
    chat_memory[conversation_id].append({"role": "user", "content": current_user_text})

    # Call LLaMA API to extract intent/entities
    llm_response = query_gpt_api(chat_memory[conversation_id])

    if llm_response is None:
        llm_response = "Sorry, something went wrong."
 

    if isinstance(llm_response, dict) and llm_response.get("structured_data"):
        # convert string to dict and build the embedded document
        try:
            structured_query = llm_response["structured_data"]
            print("Structured Query Extracted:", structured_query)
            #print(process_search(structured_query))
            #return process_search(structured_query)

        except json.JSONDecodeError:
            print("❌ Could not parse structured query:", structured_query)
    
    # Extract Assistant action if present
    assistant_text = llm_response if isinstance(llm_response, str) else llm_response.get("user_text", str(llm_response))

    # Save LLM response to conversation history
    chat_memory[conversation_id].append({"role": "assistant", "content": assistant_text})
    # Save last message to session for state persistence
    return {"result": llm_response}


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