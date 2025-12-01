import sys, builtins, logging

# silence stdout BEFORE anything else can run
logging.basicConfig(stream=sys.stderr)
_builtin_print = print
def print(*a, **k): _builtin_print(*a, file=sys.stderr, **k)
builtins.print = print

from fastmcp import FastMCP
import sys, os, builtins
import logging
import json
from typing import Any



from mcps.orchestrator_mcp.llm.gpt_client import query_gpt_api
from mcps.product_v_search.main import process_search
from mcps.product_v_search.main import upsert_products


from mcps.inventory_management.inventory_manager import insert_new_product_sql, get_products_variants_with_images, inventory_manager, fetch_variants_by_variant_id_sql
from mcps.analytics.data_reports_manager import data_reports_mgr

from mcps.db.models.provider import Provider
#from mcps.supplier_management.mail_providers import mail_providers as send_mail_providers
#from mcps.supplier_management.get_providers import get_providers, get_provider_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVICE_TOKEN = os.getenv("MCP_SERVICE_TOKEN", "change-me")

mcp = FastMCP("orchestrator")



# ------------------------------------------------------
# Tools
# ------------------------------------------------------
@mcp.tool
def route_request(
    action: str, 
    arguments:str| None= None, 
    products: Any | None = None,
    user_query: Any | None = None,
    conversation_id: str | None = None): 
    """
    Route incoming requests to appropriate handlers based on action name.
    """  

    if isinstance(user_query, str):
        user_query = json.loads(user_query)

    if isinstance(products, str):
        products = json.loads(products)

    result = None  

    if action == "insert_product":        # Insert new product into SQL database
        #try:
        new_variants_list = insert_new_product_sql(products or {})
        #    variants_metadata = new_variants_list["variants_per_product"]
        # except Exception as e:
        #   return {"error": f"Failed to insert product into SQL db: {str(e)}"}
        # print({"Products added to SQL with ids ": new_variants_list["SQL_inserted_product_ids"]})
        # print({"Variants added to SQL with ids ": new_variants_list["SQL_inserted_product_variants_ids"]})
        # #result = {"message": "Insert product not implemented"}
        # result = {"Products added to SQL db ": upsert_products(variants_metadata or {})}  ## Product vector db insertion 
    
    elif action == "delete_variant_by_sku":
        try:
           result = inventory_manager(user_query or {}, action)
        except Exception as e:
          return {"error": f"Failed to delete product variant: {str(e)}"} 
        
    elif action == "delete_product_by_id":
        try:
           result = inventory_manager(user_query or {})
        except Exception as e:
          return {"error": f"Failed to delete product: {str(e)}"} 
    elif action == "fetch_products":
        try:
            return get_products_variants_with_images()
        except Exception as e:
            return {"error": f"Failed to fetch products and variants: {str(e)}"}

    elif action == "report":
        try:
            result = data_reports_mgr(user_query or {})
        except Exception as e:
            return {"error": f"Failed to process data report: {str(e)}"}
    elif action == "health":
        result= health()
    elif action == "echo":
        message = arguments.get("message", "")
        result= echo(message)
    else:
        return {"error": f"Unknown action: {action}"}


    text_output = json.dumps(result, indent=2) # Serialize to pretty JSON
    # Claude MCP-compatible content block format
    return {
        "content": [
            {
                "type": "text",
                "text": text_output
            }
        ]
    }


@mcp.tool()
def semantic_product_search( 
    user_query: Any | None = None,
    conversation_id: str | None = None): 

    try:
        result = process_vector_search(conversation_id, user_query or {})

    except Exception as e:
        return {"error": f"Failed to process vector search: {str(e)}"}
    
    text_output = json.dumps(result, indent=2) # Serialize to pretty JSON
        # Claude MCP-compatible content block format
    return {
        "content": [
            {
                "type": "text",
                "text": text_output
            }
        ]
    }


@mcp.tool()
def create_analytics_dashboard(action: str, user_query: Any | None = None):
    """
    Create an interactive analytics artifact
    """
    if isinstance(user_query, str):
        user_query = json.loads(user_query)
    if action == "report":
        # Return React component code
        text_output = json.dumps(data_reports_mgr(user_query or {}), indent=2) # Serialize to pretty JSON
        return {
            "content": [
                {
            "artifact_type": "react",
            "code": text_output
                }
    ]
        }


@mcp.tool()
def mail_providers_tool(user_query: Any | None = None):   
    """
    Contact providers via email.
    """
    if isinstance(user_query, str):
        user_query = json.loads(user_query)



    user_query = user_query or {}  # Ensure user_query is a dictionary
    subject = (user_query or {}).get("subject", "No Subject")
    body = (user_query or {}).get("body", "No Body")
    to_emails = (user_query or {}).get("to_emails", [])

    result = send_mail_providers(subject, body, to_emails)
    return {"result": result}


@mcp.resource("providers://all")
def get_all_providers():
    """
    Fetch all providers from the database.
    """
    return get_providers()

@mcp.resource("provider_email://by_id/{provider_id}")
def get_provider_mail_by_id(provider_id: int):
    """
    Fetch a provider email by provider ID.
    """
    return get_provider_email(provider_id)


# ------------------------------------------------------

chat_memory={} # Dict[str, List[Dict[str, str]]]

def process_vector_search(conversation_id:str, user_query: dict):
    """
    Perform a semantic search for products based on user query.
    """

    if conversation_id not in chat_memory:
        chat_memory[conversation_id] = []

    # Add user query to conversation history
    current_user_text = user_query.get('query', '')
    chat_memory[conversation_id].append({"role": "user", "content": current_user_text})

    # Call gpt model to extract intent/entities
    llm_response = query_gpt_api(chat_memory[conversation_id])

    if llm_response is None:
        llm_response = "Sorry, something went wrong."
 
    if isinstance(llm_response, dict) and llm_response.get("structured_data"):
        # do vector search..
        try:
            structured_query = llm_response["structured_data"]  
            print("Structured Query Extracted from Chatbot:", structured_query)
        except json.JSONDecodeError:
            print("❌ Could not parse structured query:", structured_query)

        matched_results = process_search(structured_query)
        # return products from sql
        print("Matched results", matched_results)
        fetched_variants = fetch_variants_by_variant_id_sql(matched_results["variant_ids_ranked"])
        
        summary = []
        # create a map (fast lookup)
        reasons_by_id = {
            item["variant_id"]: item.get("reason", "") for item in matched_results["ranked_list"]
        }
        # build a summary object to provide search context to chatbot
        for v in fetched_variants["variants"]:
            item = {
                "variant_id": v["variant_id"],
                "name": v["name"],
                "tags_string": v["tags_string"],
                "price": v["price"],
                "reason": reasons_by_id.get(v["variant_id"], None)
            }
            summary.append(item)

        # Convert to JSON string (LLM-safe formatting)
        json_summary = json.dumps(summary)
        # Save LLM response to conversation history
        chat_memory[conversation_id].append({
            "role": "system", 
            "content": f"Be aware of the search results populated to user: <search_results>{json_summary}</search_results>. Provide short answer with some of the matching criteria"})
        llm_response = query_gpt_api(chat_memory[conversation_id])
        return {"llm_response": llm_response,
                "fetched_results": fetched_variants,
                }
    
    # Extract Assistant action if present
    assistant_text = llm_response if isinstance(llm_response, str) else llm_response.get("user_text", str(llm_response))

    # Save LLM response to conversation history
    chat_memory[conversation_id].append({"role": "assistant", "content": assistant_text})
    # Save last message to session for state persistence
    return {"llm_response": llm_response,
            "fetched_results": [],
            }


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
    
    #print("FastMCP Orchestrator started on port 8000")
    mcp.run(transport="http", host="0.0.0.0", port=8000)
    
    #mcp.run(transport="http", host="127.0.0.1", port=8000) # Use this for local 
    
    ###### Use stdio transport for Claude Desktop ######
    #print("FastMCP Orchestrator started with stdio transport", file=sys.stderr)
    #mcp.run(transport="stdio")