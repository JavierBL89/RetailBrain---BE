import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def query_llama_api(context: str) -> str:
    """
    Query the LLaMA API with the given context.
    """

    if context is None or context == " " or not isinstance(context, str):
        return "No context provided"

    custom_message = "Sorry, Llama model is not available right now."

    API_URL = "https://router.huggingface.co/v1/chat/completions"

    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
            "Content-Type": "application/json"
        }
        payload = {
            "temperature": 0.1,
            "messages": [
                {
                "role": "system", 
                 "content": 
                 """
                   ### Role
                   You are a helpful assistant for an e-commerce platform. 

                   ### Instructions
                   - Your task is to extract the user intent from the user's query and the entities mentioned in the query.
                   - The user intent can be searching for products, asking for product details, comparing products, etc.
                   - The entities can be product names, categories, brands, attributes, etc.
                   - The query might contain price ranges (e.g., under $50, between $20 and $100).
                   - Provide the output in JSON format with two keys: "intent", "entities", "price" and "price_range".
                   - Do not invent any entities that are not mentioned in the query.
                   - Don not generate any extra text outside the JSON format.

                   ### Price range table mapping
                    | Phrase                                          | Operator   |
                    |-----------------------                          |------------|
                    | "under" - "less than" - "no more than"          |  <=        |
                    | "between $ and $" - "more than $ and less than" | >= <=      |
                    | "around" -  "exactly"                           | =          |
                    | "over" - "more than" - "greater than"           | >=         |
                    | "exactly"                                       | =          |


                   ### Example
                     User Query: "Find me some running shoes from Nike under $100."
                     Output:{"intent": "search_products", "entities": {"running shoes Nike}, "price": 100, "price_range": "<="}

                    ### Example
                    User Query: "I'm looking for a red shoes for a night out to combine with my red dress between $50 and $150."
                    Output:{"intent": "search_products", "entities": {"red shoes night out}, "price": 100, "price_range": "<="}

                    ### Example
                    User Query: "Do you have a comfortable light color sandals? the ones with velcro straps and flat sole, no heel"
                    Output:{"intent": "search_products", "entities": {"light color sandals velcro flat sole no heel}, "price": 0, "price_range": ""}


                    ### Example
                    User Query: "Do you have a comfortable light color sandals? the ones with velcro straps and flat sole, no heel"
                    Output:{"intent": "search_products", "entities": {"light color sandals velcro flat sole no heel}, "price": 0, "price_range": ""}

                    Example
                    User Query: "Do you have white sneakers for kids?"
                    Output: {"intent": "search_products", "entities": {"white sneakers kids"}, "price": 0, "price_range": ""}
                 """
                 },
               {
                 "role" : "user",
                 "content" : context
               }
            ],
            "model": "meta-llama/Meta-Llama-3-8B-Instruct:novita",
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            response_json = response.json()
            print("Response JSON:", response_json)
            return response_json['choices'][0]['message']['content']
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return custom_message
        

    except Exception as e:
        print (f"Error generating payload from LLaMA API: {e}")
        return custom_message