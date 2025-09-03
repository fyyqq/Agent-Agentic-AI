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

messages = [
    {"role": "system", "content": "You are a math tutor"},
    {"role": "user", "content": input_from_user() }
]

# First exchange
response1 = generate_response(messages)
print(f"Response 1: {response1}")

# Get previous conversation
messages.append({"role": "assistant", "content": response1})

# Continue conversation
messages.append({"role": "user", "content": input_from_user() })
response2 = generate_response(messages)
print(f"Response 2: {response2}")

# Get previous conversation
messages.append({"role": "assistant", "content": response2})

# Keep building...
messages.append({"role": "user", "content": input_from_user()})
response3 = generate_response(messages)
print(f"Response 3: {response3}")

