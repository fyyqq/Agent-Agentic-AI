from openai import OpenAI
import anthropic
import google.generativeai as genai

def generate_response_multi_provider(messages):
    # Try OpenAI first
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return {"provider": "openai", "response": response.choices[0].message.content}
    
    except Exception as e:
        print(f"OpenAI failed: {e}")
    
    # Fallback to Claude
    try:
        client = anthropic.Anthropic()
        # Convert OpenAI format to Claude format
        claude_messages = convert_to_claude_format(messages)
        
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=claude_messages
        )
        return {"provider": "claude", "response": message.content[0].text}
    
    except Exception as e:
        print(f"Claude failed: {e}")
    
    # Fallback to Gemini
    try:
        genai.configure(api_key="your-gemini-key")
        model = genai.GenerativeModel('gemini-pro')
        
        # Convert to Gemini format
        prompt = messages[-1]["content"]
        response = model.generate_content(prompt)
        return {"provider": "gemini", "response": response.text}
    
    except Exception as e:
        print(f"Gemini failed: {e}")
    
    return {"provider": "none", "response": "All providers failed"}