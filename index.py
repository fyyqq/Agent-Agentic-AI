import os
import json
import dotenv as env
from openai import OpenAI
from typing import List, Dict
from litellm import completion

env.load_dotenv()
token = os.getenv("GPT_4_API_KEY")  # Use the GPT-4 API key from .env
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def generate_response(messages: List[Dict]) -> str:
    print("\nCall LLM to get response...\n\n")

    response = client.chat.completions.create(
        messages=messages,
        max_tokens=1024,
        temperature=1,
        top_p=1,
        model=model
    )

    return response.choices[0].message.content

messages = [
    {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
    {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
# print(response)

# Second query without including the previous response
messages = [
    {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
    {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."},

    {"role": "assistant", "content": response},

    {"role": "user", "content": "Update the function to include documentation."}
]

response = generate_response(messages)
print(response)