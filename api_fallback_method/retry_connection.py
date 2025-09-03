import time
import random

def generate_response_smart_fallback(messages, max_retries=3):
    providers = [
        {"name": "openai", "model": "gpt-4", "client": OpenAI()},
        {"name": "openai", "model": "gpt-3.5-turbo", "client": OpenAI()},
        # Add other providers here
    ]
    
    for provider in providers:
        for attempt in range(max_retries):
            try:
                # Add exponential backoff
                if attempt > 0:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"⏳ Waiting {wait_time:.1f}s before retry...")
                    time.sleep(wait_time)
                
                response = provider["client"].chat.completions.create(
                    model=provider["model"],
                    messages=messages,
                    max_tokens=1024,
                    timeout=30  # Add timeout
                )
                
                print(f"✅ Success: {provider['name']} - {provider['model']}")
                return response.choices[0].message.content
                
            except Exception as e:
                error_msg = str(e).lower()
                
                # Handle specific errors
                if "rate_limit" in error_msg:
                    print(f"⏱️ Rate limited on {provider['name']}, trying next...")
                    break  # Skip to next provider
                elif "invalid_api_key" in error_msg:
                    print(f"🔑 Invalid key for {provider['name']}, skipping...")
                    break  # Skip to next provider
                else:
                    print(f"❌ Attempt {attempt+1} failed: {str(e)}")
                    continue  # Retry same provider
    
    return "All fallback options exhausted"