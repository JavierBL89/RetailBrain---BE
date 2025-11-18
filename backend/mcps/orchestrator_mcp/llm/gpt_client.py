import json
import requests
from dotenv import load_dotenv
import os
import logging
from openai import OpenAI
import re


client = OpenAI() # Automatically picks up OPENAI_API_KEY. The SDK internally runs something like: os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)
load_dotenv()



def query_gpt_api(context: str) -> str:
    """
    Query the LLaMA API with the given context.
    """

    if context is None or context == " " or not isinstance(context, str):
        return "No context provided"


    try:
        # response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        
        response= client.responses.create(
            prompt={
                "id": "pmpt_691b370b69a8819488c4df0af9dfe6880f6df17c89108ed1",
                "version": "2"
            },
            model="gpt-4o-mini",
            temperature=0.1,
            top_p=0.9,
            input= [{"role" : "user","content" : context}],
        )

        if response is not None:
            logging.info("Response JSON:", response)
            
            result = response.output_text.strip()
            # Split chat output from structured JSON if present
            return trim_output_helper(result)

        else:
            logging.info("Error: No response received from OpenAi API")
            return custom_message
        

    except Exception as e:
        print(f"❌ Error querying model: {e}")
        return {
            "user_text": "Sorry, something went wrong.",
            "structured_data": None
        }

    

def trim_output_helper(gpt_full_output : str):

     # --- Split structured JSON if present ---
        json_match = re.search(r"\{[\s\S]*\}$", gpt_full_output)
        structured_data = None

        if json_match:
            json_part = json_match.group(0)
            try:
                structured_data = json.loads(json_part)
                # Trim the text before JSON for user display
                user_text = gpt_full_output[:json_match.start()].strip()
            except json.JSONDecodeError:
                user_text = gpt_full_output
        else:
            user_text = gpt_full_output

        # --- Return both ---
        return {
            "user_text": user_text,
            "structured_data": structured_data
        }
