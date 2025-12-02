
##THE FIX: Monkey-patch print() safely
import builtins
_real_print = builtins.print

def safe_print(*args, **kwargs):
    # Remove conflicting 'file' kwarg injected by dependencies
    kwargs.pop("file", None)
    _real_print(*args, **kwargs)

builtins.print = safe_print



import logging
import json
from pathlib import Path
import chromadb
import sys
import ast

ROOT = Path(__file__).resolve().parents[2]
print("ROOT:", ROOT)
sys.path.append(str(ROOT))

from mcps.product_v_search.embedding_client import embedding_client
from mcps.product_v_search.llm.gpt_client import products_ranker, trim_output_helper

from mcps.product_v_search.embedding_client import embedding_client

# Get directory of THIS file (absolute)
BASE_DIR = Path(__file__).resolve().parent

PERSIST_DIR = BASE_DIR / "chroma_db"
client = chromadb.PersistentClient(path=str(PERSIST_DIR)) ## creates database
collection = client.get_or_create_collection("products_db",    ## creates colleltion if not exists
                                   metadata={"hnsw:space": "cosine"})  # recommended for text embeddings



# ------------------------------------------------------
# MODULE FUNCTIONS
# ------------------------------------------------------

def upsert_products(products: dict | list) -> str:
    """
    Insert one or many products into the inventory system.
    Automatically handles batching for fast insertion.
    """
    print("Upsert Products Called with:", products)


    logging.info("=" * 40)
    logging.info("📦 BATCH UPSERT PRODUCT REQUEST")
    logging.info("=" * 40)
    logging.info(json.dumps(products, indent=2))
    logging.info("=" * 40)

    # --- Prepare batch fields ---
    variant_ids_to_check = [str(p["variant_id"]) for p in products]
    print("Product IDs to check:", variant_ids_to_check)
    # Check existing products in one call
    existing = collection.get(ids=variant_ids_to_check)
    print("Existing products found:", existing)
    existing_ids = set(existing["ids"]) if existing and existing["ids"] else set()
    print("Existing product IDs to delete:", existing_ids)
    # Delete all existing variant_ids at once
    if existing_ids:
        collection.delete(ids=list(existing_ids))
        print(f"Deleted {len(existing_ids)} existing products before upsert.")
    # Lists for batch insert
    new_variant_ids = []
    new_docs = []
    new_vectors = []
    print(f"Preparing to upsert {len(products)} products...")

    # --- Process Each Product ---
    for product in products:
        variant_id = product["variant_id"]
        print("Processing product:", variant_id)

        document_text = (
            f"brand: {product.get('brand', '')}, "
            f"category: {product.get('category', '')} {product.get('category', '')}, "
            f"color: {product.get('color', '')}, "
            f"material: {product.get('material', '')}, "
            f"price: {product.get('price', '')}, "
            f"heel-type: {product.get('heel-type', '')}, "
            f"heel-height: {product.get('heel-height', '')}, "
            f"tags_string: {product.get('tags_string', '')} {product.get('tags_string', '')}, "
            f"occasion: {product.get('occasion', '')} occasion"
        )

        print("Embedding product:", document_text)
        vector = embedding_client.embed_product_document(document_text)
        if vector is None:
            raise ValueError(f"Failed to generate embedding for product {variant_id}")

        new_variant_ids.append(str(variant_id))
        new_docs.append(document_text)
        new_vectors.append(vector)
        print(f"Prepared product {variant_id} for upsert.")

    # --- Single batch DB insert ---
    collection.add(
        ids=new_variant_ids,
        documents=new_docs,
        embeddings=new_vectors
    )

    print(f"{len(products)} Products Added Successfully to ChromaDB")

    return json.dumps({
        "status": "success",
        "message": f"{len(products)} product(s) logged successfully",
        "count": len(products),
        "products": products
    }, indent=2)



def process_search(bot_query: dict):
    """
    Perform a semantic search for products based on the bot_query.
    """
    # 1. Build weighted query text for embeddings
    document = build_query_document(bot_query)
    
    # 2. Extract query keywords from metadata
    keywords = extract_query_keywords(bot_query)

    # 3. Build dynamic where_document filter
    where_doc = build_dynamic_where_document(keywords)
    print("Built Query Document:", document)

    # 4. Embed the text query
    embedded_document = embedding_client.embed_user_query(document)

    # 5. Perform semantic search and rerank results
    matched_variants = semantic_search(embedded_document, where_doc, document)

    if not matched_variants:
        return {
            "status": "success",
            "results": [],
            "message": "No matching products found."
        }
    print("Matched_variants found in Chromadb", matched_variants)

    # 7. Rank products with LLM
    ranked_data= rank_products_with_llm(document, matched_variants)
    print("LLM Response Ranked Data", ranked_data)

    # 8. Order results based on ranking
    ranked_list = ranked_data["structured_data"]["ranked"]

    # Sanitize scores returned by GPT ---
    for i, item in enumerate(ranked_list):
        try:
            item["score"] = float(item["score"])
        except Exception:
            print("⚠️ Invalid score from LLM. Forcing score=999:", item)
            item["score"] = 999

    variant_ids_ranked = [str(item["variant_id"]) for item in ranked_list]
    
    return{
        "status": "success",
        "ranked_list": ranked_list,
        "variant_ids_ranked": variant_ids_ranked
    }


def rank_products_with_llm(document: str, matched_variants: list):
    """
    Rerank products using LLM based on the search document.
    """

    # Call LLM to rank products 
    ranked_json = products_ranker(document, matched_variants)

   # --- Handle both str and dict safely ---
    if isinstance(ranked_json, dict):
        # Already parsed JSON
        ranked_data = ranked_json

    elif isinstance(ranked_json, str):
        # Try to parse JSON string from LLM
        try:
            ranked_data = ast.literal_eval(ranked_json)  # ← SAFE FIX HERE
        except json.JSONDecodeError:
            # If LLM returned mixed chat + JSON, extract JSON part
            cleaned = trim_output_helper(ranked_json)
            try:
                ranked_data = ast.literal_eval(cleaned) ## convert to a dict
            except:
                ranked_data = {"error": "Could not parse LLM output", "raw": ranked_json}
    else:
        ranked_data = {"error": "Unexpected LLM output type", "raw_type": str(type(ranked_json))}
    
    return  ranked_data



def extract_query_keywords(bot_query):
    """
    Extract keywords from bot_query metadata for filtering.
    """
    keywords = []
    metadata = bot_query.get("metadata", {})

    for key, value in metadata.items():
        if not value:
            continue

        parts = str(value).replace(",", " ").split()

        for p in parts:
            p = p.strip().lower()
            if p:
                keywords.append(p)

    return keywords


def build_dynamic_where_document(keywords):
    """
    Build a dynamic where_document filter for ChromaDB based on keywords.
    """
    if not keywords:
        return None
    return {
        "$or": [
            {"$contains": k} for k in keywords
        ]
    }


def semantic_search(embedded_document: list[float], where_doc: dict | None, document: str):
    """
    Perform semantic search in ChromaDB with optional filtering.
    """

    results = collection.query(
        query_embeddings=[embedded_document],
        n_results=5,
        where_document=where_doc,
        include=["documents", "distances"]
    )

    if not results["ids"] or not results["ids"][0]:
        return {
            "status": "success",
            "results": [],
            "message": "No similar products found"
        }

    return results
    

def build_query_document(bot_query: dict):
    """
    Build a weighted query document from bot_query metadata.
    """
    parts = []
    QUERY_WEIGHTS = {
        "brand": 1,
        "color": 3,
        "category": 4,
        "heel-type": 2,
        "heel-height": 2,
        "sole_type": 1,
        "tags_string": 2,
        "occasion": 2,
    }
    metadata = bot_query.get("metadata", {})
    for key, value in metadata.items():
        if not value:
            continue

        # Get weight for this field
        weight = QUERY_WEIGHTS.get(key, 1)
        repeated = " ".join([value] * weight) # Repeat value based on weight

        parts.append(f"{key}: {repeated}")

    return ", ".join(parts) + "."



def delete_all_products():
    """
    Delete all products from the collection.
    """
    all_variant_ids = collection.get()['variant_ids']
    if all_variant_ids:  # Only call delete if there are variant_ids
        collection.delete(variant_ids=all_variant_ids)
        logging.info("All products deleted from the collection.")
    else:
        logging.info("No products to delete.")



if __name__ == "__main__":


#      products_list = [
#      {
#          "variant_id": "9",
#              "brand": "Aldo",
#              "category": "Shoes",
#              "color": "Black",
#              "material": "Synthetic Leather",
#              "heel-type": "wedge",
#              "heel-height": "medium",
#              "tags_string": "black wedge, mary jane style, ankle strap, synthetic leather, casual wear, dress shoes, platform wedge, comfortable heel, aldo, women's shoes",
#              "occasion": "casual wear, dress shoes, work, office"
#      },
#      {
#          "variant_id": "10",
#              "brand": "Aldo",
#              "category": "Shoes",
#              "color": "Black",
#              "material": "Synthetic Leather",
#              "heel-type": "block",
#              "heel-height": "medium",
#              "tags_string": "black patent leather, mary jane style, block heel, ankle strap, synthetic leather, casual wear, dress shoes, formal wear, glossy finish, aldo, women's shoes, low-heel, medium-heel",
#              "occasion": "casual wear, dress shoes, formal wear"
#      },
#      {
#          "variant_id": "11",
#              "brand": "Clarks",
#              "category": "Shoes",
#              "color": "Red",
#              "material": "Leather",
#              "heel-type": "stiletto",
#              "heel-height": "high",
#              "tags_string": "red peep toe, studded heels, stiletto heel, leather, formal wear, special occasion, dress shoes, statement heels, high-heel, clark, women's shoes",
#              "occasion": "formal wear, special occasion, dress shoes"
#      },
#      {
#          "variant_id": "12",
#              "brand": "Clarks",
#              "category": "Boot",
#              "color": "Black",
#              "material": "Synthetic Leather",
#              "heel-type": "stiletto",
#              "heel-height": "high",
#              "tags_string": "black ankle boot, high heel boot, synthetic leather, formal wear, stiletto heel, platform boot, side zipper, dress boots, clarks, women's boots",
#              "occasion": "formal wear, dress boots"
#      },
#      {
#          "variant_id": "13",
#              "brand": "Aldo",
#              "category": "Platform-Shoes",
#              "color": "Black",
#              "material": "Suede",
#              "heel-type": "stiletto",
#              "heel-height": "high",
#              "tags_string": "black platform heels, synthetic suede, stiletto heel, platform pumps, formal wear, dress shoes, high heel, slip-on, aldo, women's platform shoes",
#              "occasion": "formal wear, dress shoes, casual wear"
#      },
#      {
#          "variant_id": "14",
#              "brand": "Clarks",
#              "category": "Sandals",
#              "color": "Orange",
#              "material": "Synthetic Leather",
#              "heel-type": "stiletto",
#              "heel-height": "high",
#              "tags_string": "orange platform sandal, strappy heels, synthetic leather, stiletto heel, dress shoes, special occasion, party heels, high heel sandal, clarks, women's platform sandals",
#              "occasion": "dress shoes, special occasion, party, celebration, event"
#      },
#      {
#          "variant_id": "15",
#              "brand": "Clarks",
#              "category": "Shoes",
#              "color": "Red",
#              "material": "Synthetic",
#              "heel-type": "stiletto",
#              "heel-height": "high",
#              "tags_string": "red peep toe, embellished heels, synthetic leather, stiletto heel, high-heel, special occasion, dress shoes, party heels, studded toe, clarks, women's heels",
#              "occasion": "special occasion, dress shoes, party, celebration, event"
#      },
#      {
#          "variant_id": "16",
#              "brand": "Aldo",
#              "category": "Shoes",
#              "color": "Red",
#              "material": "Synthetic Leather",
#              "heel-type": "wedge",
#              "heel-height": "low",
#              "tags_string": "brown wedge, mary jane style, ankle strap, synthetic leather, aldo, platform, casual wear, dress shoes, platform wedge, low-heel, comfortable heel, aldo, women's shoes",
#              "occasion": "casual wear, dress shoes"
#      },
#      {
#          "variant_id": "17",
#              "brand": "Zara",
#              "category": "Sandals",
#              "color": "Black",
#              "material": "Synthetic",
#              "heel-type": "block",
#              "heel-height": "medium",
#              "tags_string": "black studded sandal, clear strap heels, transparent straps, synthetic leather, special occasion, dress shoes, party, medium-heels, block heel, zara, women's sandals",
#              "occasion": "special occasion, dress shoes, party, celebration, event"
#      },
#      {
#          "variant_id": "18",
#              "brand": "Zara",
#              "category": "Sandals",
#              "color": "Gold",
#              "material": "Synthetic",
#              "heel-type": "wedge",
#              "heel-height": "low",
#              "tags_string": "gold wedge sandal, clear straps, transparent heels, synthetic leather, special occasion, dress shoes, low-heel, party heels, minimalist design, zara, women's wedge sandals",
#              "occasion": "special occasion, dress shoes, party, celebration, event"
#      },
#      {
#          "variant_id": "20",
#              "brand": "Aldo",
#              "category": "Comfort-Sandals",
#              "color": "Black",
#              "material": "Synthetic",
#              "heel-type": "flat",
#              "heel-height": "low",
#              "tags_string": "comfort sandals, walking shoes, adjustable straps, black, synthetic leather, casual wear, velcro straps, cushioned footbed, everyday comfort, aldo, women's comfort shoes",
#              "occasion": "casual wear, everyday comfort"
#      },
#      {
#          "variant_id": "19",
#              "brand": "Aldo",
#              "category": "Sandals",
#              "color": "Beige",
#              "material": "Synthetic",
#              "heel-type": "flat",
#              "heel-height": "low",
#              "tags_string": "comfort sandals, walking shoes, adjustable straps, beige, synthetic leather, casual wear, velcro straps, cushioned footbed, everyday comfort, aldo, women's comfort shoes",
#              "occasion": "casual wear, everyday comfort"
#      },
#      {
#          "variant_id": "22",
#              "brand": "Aldo",
#              "category": "Boots",
#              "color": "Black",
#              "material": "Synthetic Leather",
#              "heel-type": "flat",
#              "heel-height": "low",
#              "tags_string": "black riding boot, low heel boot, synthetic leather, casual wear, everyday comfort, knee-high boot, side zipper, equestrian style, aldo, women's boots",
#              "occasion": "casual wear, everyday comfort"
#      },
#      {
#          "variant_id": "23",
#              "brand": "Aldo",
#              "category": "Boots",
#              "color": "Cognac",
#              "material": "Synthetic Leather",
#              "heel-type": "block",
#              "heel-height": "medium",
#              "tags_string": "cognac riding boot, low heel boot, synthetic leather, casual wear, everyday comfort, knee-high boot, zipper, equestrian style, aldo, women's boots",
#              "occasion": "casual wear, everyday comfort"
#      },
#      {
#          "variant_id": "21",
#              "brand": "Zara",
#              "category": "Boots",
#              "color": "Brown",
#              "material": "Synthetic Leather",
#              "heel-type": "stiletto",
#              "heel-height": "high",
#              "tags_string": "brown knee-high boot, block heel, synthetic leather, dress boots, casual wear, high top boot, zipper, fashion boots, zara, women's boots",
#              "occasion": "casual wear, dress boots"
#      }
#  ]
#      upsert_products(products_list)
      print("Prodcut v Search running")