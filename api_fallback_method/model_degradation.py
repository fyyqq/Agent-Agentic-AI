def generate_response_with_model_fallback(messages):
    models = [
        ("gpt-4", "premium"),
        ("gpt-3.5-turbo", "standard"), 
        ("gpt-3.5-turbo-instruct", "basic")
    ]
    
    for model, tier in models:
        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1024
            )
            print(f"✅ Success with {model} ({tier})")
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"❌ {model} failed: {str(e)}")
            continue
    
    return "All models failed"