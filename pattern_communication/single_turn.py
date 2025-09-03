import os
import json
import dotenv as env
from openai import OpenAI
from typing import List, Dict

env.load_dotenv()
token = os.getenv("QWEN_3_API_KEY")
model = "qwen/qwen3-coder:free",
endpoint = "https://openrouter.ai/api/v1"


# OpenAI
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def generate_response(messages: List[Dict]) -> str:
    f"""Call {model} API to get response"""
    print("\n🤔 LLM is thinking...\n")
    
    try:
        # OpenAI connection
        response = client.chat.completions.create(
            messages=messages,
            max_tokens=1024,
            temperature=0.7,  # Slightly creative but focused
            model=model
        )

        return response.choices[0].message.content
    
    except Exception as e:
        print(f"❌ Error calling {model} API: \n{str(e)}\n")
        # Fallback response
        return "Sorry, I'm having trouble connecting right now."


user_input = input("\n👤: ").strip()
user = user_input if user_input != "" else "say Hello"

messages = [
    {"role": "system", "content": "You are a helpful assistant, answer & keep it simple"},
    {"role": "user", "content": user}
]
response = generate_response(messages)
print(f"🤖: {response}\n")

