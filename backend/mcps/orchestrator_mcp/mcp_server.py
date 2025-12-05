import sys, builtins
import logging
# silence stdout BEFORE anything else can run
logging.basicConfig(stream=sys.stderr)
_builtin_print = print
def print(*a, **k): _builtin_print(*a, file=sys.stderr, **k)
builtins.print = print

from fastmcp import FastMCP
import sys, os, builtins
import json
from typing import Any



from mcps.orchestrator_mcp.llm.gpt_client import query_gpt_api
from mcps.product_v_search.main import process_search
from mcps.product_v_search.main import upsert_products


from mcps.inventory_management.inventory_manager import insert_new_product_sql, get_products_variants_with_images, inventory_manager, fetch_variants_by_variant_id_sql, get_low_stock_product_variants, inv_mang_module_info
from mcps.analytics.data_reports_manager import data_reports_mgr

from mcps.db.models.provider import Provider
from mcps.supplier_management.mail_providers import send_email_providers
from mcps.supplier_management.get_providers import get_all_providers, get_provider_email, supplier_management_info

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVICE_TOKEN = os.getenv("MCP_SERVICE_TOKEN", "change-me")

mcp = FastMCP("orchestrator")



# ------------------------------------------------------
# Tools
# ------------------------------------------------------
@mcp.tool()
def inventory_management( 
    action: str, 
    arguments:str| None= None, 
    user_query: Any | None = None,
    products: Any | None = None):
     
    if isinstance(products, str):
        products = json.loads(products)

    result = None  

    if action == "inv_mang_module_info":
            return inv_mang_module_info()
    
    elif action == "insert_product": 
        logger.info("inserting product")
        try: # Insert new product into SQL database
            new_variants_list = insert_new_product_sql(products or {})
            variants_metadata = new_variants_list["variants_per_product"]
        except Exception as e:
            return {"error": f"Failed to insert product into SQL db: {str(e)}",
                        "details": str(e)
                    }
        # Insert new product into Chromadb
        result =  upsert_products(variants_metadata or {})  ## Product vector db insertion 


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
        

    elif action == "get_low_stock_product_variants":
        try:
            return get_low_stock_product_variants(user_query or {})
        
        except Exception as e:
            return {"error": f"Failed to fetch products and variants: {str(e)}"}


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


@mcp.tool
def analytics_operations(
    action: str, 
    arguments:str| None= None, 
    user_query: Any | None = None): 
    """
    Route incoming requests to appropriate handlers based on action name.
    """  

    if isinstance(user_query, str):
        user_query = json.loads(user_query)

    if action == "report":
        try:
            result = data_reports_mgr(user_query or {})
        except Exception as e:
            return {"error": f"Failed to process data report: {str(e)}"}
        
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
def supplier_management(action: str |None = None, 
                        user_query: Any | None = None):   
    """
    Contact providers via email.
    """

    if action=="describe":
        return supplier_management_info()
    
    if isinstance(user_query, str):
        user_query = json.loads(user_query)

    result = None

    if action == "get_providers_list":
        result = get_all_providers()

    if action == "get_provider_email":
        pid = (user_query or {}).get("provider_id")
        result = get_provider_email(pid)
    
    if action == "send_email_providers":
        subject = (user_query or {}).get("subject", "No Subject")
        body = (user_query or {}).get("body", "No Body")
        to_email = (user_query or {}).get("to_emails", [])

        result = send_email_providers(subject, body, to_email)

    return {"result": result}


# ------------------------------------------------------
#   PROMPTS DISPACHERS
# ------------------------------------------------------
@mcp.prompt()
def supplier_management():

    name = "mail_providers_prompt.txt"
    return load_prompt(name)

@mcp.prompt()
def inventory_management():
    name = "inventory_management_prompt.txt"
    return load_prompt(name)

@mcp.prompt()
def sales_analytics():
    name = "sales_analytics_prompt.txt"
    return load_prompt(name)

# ------------------------------------------------------
#   HELPER FUCNTIONS
# ------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "static", "prompts"))
def load_prompt(name: str) -> str:
    """ 
    """
    file_path = os.path.join(PROMPTS_DIR, name)
    if not os.path.isfile(file_path):
        return f"Prompt filepath'{PROMPTS_DIR}/{name}' not found."
    return open(file_path).read()


git commit -m "Add prompts dispatchers - Complete 'Supplier Management' module"
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
    #mcp.run(transport="http", host="0.0.0.0", port=8000)
    
    #mcp.run(transport="http", host="127.0.0.1", port=8000) # Use this for local 
    
    ###### Use stdio transport for Claude Desktop ######
    #print("FastMCP Orchestrator started with stdio transport", file=sys.stderr)
    mcp.run(transport="stdio")