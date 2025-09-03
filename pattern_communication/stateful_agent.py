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

user_state = {
    "genre": None,
    "mood": None,
    "step": 1  # Men-track progress percakapan
}

# Fungsi untuk update state berdasarkan respons user
def update_state(user_input, current_state):
    if current_state["step"] == 1:
        current_state["genre"] = user_input
        current_state["step"] = 2
        return "What mood are you in today? (e.g., happy, sad, adventurous)"
    
    elif current_state["step"] == 2:
        current_state["mood"] = user_input
        current_state["step"] = 3
        return "Great! I'm generating recommendations based on your preferences..."
    
    return None

# Percakapan multi-turn
def stateful_agent_conversation():
    print("AI: Hi! Let me recommend a movie. What genre do you like?")
    
    while user_state["step"] < 3:
        user_input = input("You: ")
        
        # Update state berdasarkan input user
        response = update_state(user_input, user_state)
        
        if response:
            print("AI:", response)
        else:
            break
    
    # Gunakan state untuk generate rekomendasi akhir
    if user_state["step"] == 3:
        prompt = f"Recommend a movie for genre: {user_state['genre']} and mood: {user_state['mood']}. Only recommend one."
        response = generate_response(prompt)
        print("AI: Here's your recommendation:", response)

stateful_agent_conversation()