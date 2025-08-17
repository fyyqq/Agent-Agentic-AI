import os
import dotenv as env
from openai import OpenAI
from typing import List, Dict

env.load_dotenv()
token = os.getenv("GPT_4_API_KEY")  # Use the GPT-4 API key from .env
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def generate_response(messages: List[Dict]) -> str:
    try:
        print("\nCall LLM to get response...\n\n")
        response = client.chat.completions.create(
            messages=messages,
            max_tokens=1024,
            temperature=1,
            top_p=1,
            model=model
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Error:", e)
        return "Error occurred while generating response."

messages = [
    {"role": "system", "content": "You are a very rude person. Response to the user in a rude manner."},
    {"role": "user", "content": "Hi How Are You?"}
]

result = generate_response(messages)
print(result)

