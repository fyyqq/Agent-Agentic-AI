import random
from openai import OpenAI

OPENAI_KEYS = [
    "sk-key1...",
    "sk-key2...", 
    "sk-key3..."
]

def generate_response_with_key_fallback(messages):
    for api_key in OPENAI_KEYS:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=1024
            )
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Key failed: {api_key[:10]}... Error: {str(e)}")
            continue  # Try next key
    
    return "All API keys failed"