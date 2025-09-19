import os
import json
import dotenv as env
from openai import OpenAI
from typing import List, Dict
from terminal_setup import TC

env.load_dotenv()
token = os.getenv("QWEN_3_API_KEY")
model = "qwen/qwen3-coder:free",
endpoint = "https://openrouter.ai/api/v1"

# OpenAI
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# # # # # 

def list_files() -> List[str]:
    """List files in the current directory."""
    return os.listdir(".")

def read_file(file_name: str) -> str:
    """Read a file's contents."""
    try:
        with open(file_name, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found."
    except Exception as e:
        return f"Error: {str(e)}"

def terminate(message: str) -> None:
    """Terminate the agent loop and provide a summary message."""
    print(f"Termination message: {message}")

tool_functions = {
    "list_files": list_files,
    "read_file": read_file,
    "terminate": terminate
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Returns a list of files in the directory.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file in the directory.",
            "parameters": {
                "type": "object",
                "properties": {"file_name": {"type": "string"}},
                "required": ["file_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "terminate",
            "description": "Terminates the conversation. No further actions or interactions are possible after this. Prints the provided message for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                },
                "required": ["message"]
            }
        }
    }
]

agent_rules = [{
    "role": "system",
    "content": """
You are an AI agent that can perform tasks by using available tools. 

If a user asks about files, documents, or content, first list the files before reading them.

When you are done, terminate the conversation by using the "terminate" tool and I will provide the results to the user.
"""
}]

# Initialize agent parameters
iterations = 0
max_iterations = 10

user_task = input("What would you like me to do?\n👤 : ")

memory = [{"role": "user", "content": user_task}]

# The Agent Loop
while iterations < max_iterations:

    messages = agent_rules + memory

    response = client.chat.completions.create(
        messages=messages,
        max_tokens=1024,
        temperature=0.7,  # Slightly creative but focused
        model=model
    )

    if response.choices[0].message.content:
        content = response.choices[0].message.content
    
        # Parse tool call from QWEN text response
        tool_call_parsed = None
        
        # Method 1: Try to find JSON action block
        if "```action" in content:
            try:
                start = content.find("```action") + len("```action")
                end = content.find("```", start)
                json_str = content[start:end].strip()
                tool_call_parsed = json.loads(json_str)
            except:
                pass
        
        # Method 2: Fallback - detect tools from text
        if not tool_call_parsed:
            content_lower = content.lower()
            if any(phrase in content_lower for phrase in ["list_files", "list files"]):
                tool_call_parsed = {"tool_name": "list_files", "args": {}}
            elif "read_file" in content_lower or "read file" in content_lower:
                # Try to extract filename
                import re
                file_match = re.search(r'["\']([^"\']+\.[a-zA-Z0-9]+)["\']', content)
                filename = file_match.group(1) if file_match else "unknown.txt"
                tool_call_parsed = {"tool_name": "read_file", "args": {"file_name": filename}}
            elif any(phrase in content_lower for phrase in ["terminate", "done", "complete"]):
                tool_call_parsed = {"tool_name": "terminate", "args": {"message": "Task completed"}}
        
        # If tool call found, execute it
        if tool_call_parsed:
            tool_name = tool_call_parsed["tool_name"]
            tool_args = tool_call_parsed["args"]

            action = {
                "tool_name": tool_name,
                "args": tool_args
            }

            if tool_name == "terminate":
                print(f"Termination message: {tool_args['message']}")
                break
            elif tool_name in tool_functions:
                try:
                    result = {"result": tool_functions[tool_name](**tool_args)}
                except Exception as e:
                    result = {"error":f"Error executing {tool_name}: {str(e)}"}
            else:
                result = {"error": f"Unknown tool: {tool_name}"}

            print(f"Executing: {tool_name} with args {tool_args}")
            print(f"Result: {result}")
            memory.extend([
                {"role": "assistant", "content": json.dumps(action)},
                {"role": "user", "content": json.dumps(result)}
            ])
        else:
            # No tool call detected, treat as regular response
            result = content
            print(f"Response: {result}")
            break
    else:
        result = "No response content"
        print(f"Response: {result}")
        break