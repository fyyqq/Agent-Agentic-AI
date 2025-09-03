# Conversation History Injection

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


def input_from_user():
    user_input = input("\n👤: ").strip()
    result = user_input if user_input != "" else "say Hello"
    return result

# Add multiple messages at once
memory = [
    {"role": "system", "content": "Act like you're smartphone sales assistance."},
    {"role": "system", "content": "Helping customer choosing the best option for smartphone."},

    {"role": "user", "content": "I want to buy smartphone under $1500"},

    {"role": "assistant", "content": "You have all the phone list in the world"},

    {"role": "user", "content": "Compare the price"}, 

    {"role": "assistant", "content": "Let me compare... (result of comparison)"}
]

# Add new prompt
memory.extend([
    {"role": "user", "content": "Which one has the longest battery life?"},
    {"role": "user", "content": "Which camera is the best?"},
    {"role": "user", "content": "Which one best for travelling"},
    {"role": "user", "content": "Which one best for gaming"},
    {"role": "user", "content": "Which one best for durability, strong"},
    {"role": "user", "content": "Give only one answer"}
])

response = generate_response(memory)
print(f"{response}\n")