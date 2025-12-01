import os
import requests
from pathlib import Path

HF_SPACE_URL=os.getenv("HF_SPACE_EMB_URL")
HF_TOKEN=os.getenv("HF_TOKEN")


## Local paths
# location of THIS file (main.py)
BASE_DIR = Path(__file__).resolve().parent
# ALWAYS store Chroma DB INSIDE product_v_search
PERSIST_DIR = BASE_DIR / "chroma_db"

print("Using abosolute path for PERSIST_DIR:", PERSIST_DIR)


COLLECTION= "products_db"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Define remote embedding wrapper
class HFSpaceEmbeddingClient:
    """
    Wrapper to call our HF Space embedding API.
    """

    def _call_api(self, texts):
        try:
            res= requests.post("https://javierbldev89-embedding-model-all-minilm-l6-v2.hf.space/embed", headers=HEADERS, json={"texts": texts}, timeout=30)
            res.raise_for_status()
            data =res.json()
            return data.get("embeddings", None)
        except Exception as e:
            print(f"❌ Error calling HF Space embedding API: {e}")
            return None
        
    def embed_user_query(self, text: str):
        result= self._call_api([text])
        return result[0] if result else None
    
    def embed_product_document(self, metadata: str):
        result = self._call_api([metadata])   # FIX: wrap in list
        return result[0] if result else None  # FIX: return vector, not list of vectors
    

embedding_client = HFSpaceEmbeddingClient()
        
    