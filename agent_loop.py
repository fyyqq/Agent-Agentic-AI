import os
import json
import dotenv as env
from openai import OpenAI
from typing import List, Dict
# from azure.ai.inference import ChatCompletionsClient
# from azure.ai.inference.models import SystemMessage, UserMessage
# from azure.core.credentials import AzureKeyCredential

env.load_dotenv()
token = os.getenv("GPT_OSS_API_KEY")
# endpoint = "https://models.github.ai/inference"
endpoint = "https://openrouter.ai/api/v1"
# model = "openai/gpt-4.1"
model = "openai/gpt-oss-20b:free",


# OpenAI
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# Deepseek
# client = ChatCompletionsClient(
#     endpoint=endpoint,
#     credential=AzureKeyCredential(token),
# )

# Product database - simplified
PRODUCT_DATABASE = {
    "phones": [
        # iOS Phones
        {"name": "iPhone 15 Pro Max", "price": 6500, "rating": 4.9, "features": ["premium camera", "A17 Pro", "iOS", "titanium"]},
        {"name": "iPhone 15 Pro", "price": 5800, "rating": 4.8, "features": ["pro camera", "A17 Pro", "iOS", "titanium"]},
        {"name": "iPhone 15", "price": 4500, "rating": 4.8, "features": ["good camera", "A16", "iOS", "premium"]},
        {"name": "iPhone 15 Plus", "price": 5200, "rating": 4.7, "features": ["large screen", "A16", "iOS", "long battery"]},
        {"name": "iPhone 14", "price": 3800, "rating": 4.6, "features": ["solid performance", "A15", "iOS", "reliable"]},
        {"name": "iPhone 13", "price": 3200, "rating": 4.5, "features": ["good value", "A15", "iOS", "proven"]},
        {"name": "iPhone SE 3rd Gen", "price": 1800, "rating": 4.3, "features": ["compact", "A15", "iOS", "budget-friendly"]},
        {"name": "iPhone 12", "price": 2800, "rating": 4.4, "features": ["5G ready", "A14", "iOS", "affordable"]},
        
        # Android Flagship
        {"name": "Samsung Galaxy S24 Ultra", "price": 6200, "rating": 4.8, "features": ["S Pen", "200MP camera", "Android", "premium"]},
        {"name": "Samsung Galaxy S24+", "price": 5400, "rating": 4.7, "features": ["large display", "good camera", "Android", "flagship"]},
        {"name": "Samsung Galaxy S24", "price": 4200, "rating": 4.7, "features": ["compact flagship", "good camera", "Android", "premium"]},
        {"name": "Google Pixel 8 Pro", "price": 5600, "rating": 4.6, "features": ["AI photography", "pure Android", "Google AI", "camera king"]},
        {"name": "Google Pixel 8", "price": 4800, "rating": 4.5, "features": ["clean Android", "good camera", "AI features", "regular size"]},
        {"name": "OnePlus 12", "price": 4600, "rating": 4.5, "features": ["fast charging", "OxygenOS", "Android", "performance"]},
        {"name": "Xiaomi 14 Ultra", "price": 5800, "rating": 4.6, "features": ["Leica camera", "flagship specs", "Android", "photography"]},
        
        # Mid-range Android
        {"name": "Xiaomi 14", "price": 2800, "rating": 4.5, "features": ["good value", "fast charging", "Android", "mid-range"]},
        {"name": "Samsung Galaxy A55", "price": 1800, "rating": 4.2, "features": ["good display", "decent camera", "Android", "affordable"]},
        {"name": "Google Pixel 7a", "price": 2200, "rating": 4.4, "features": ["pure Android", "good camera", "budget pixel", "clean UI"]},
        {"name": "OnePlus Nord 3", "price": 2400, "rating": 4.3, "features": ["fast performance", "good value", "Android", "mid-range"]},
        {"name": "Realme GT 5", "price": 2600, "rating": 4.2, "features": ["gaming focused", "fast charging", "Android", "performance"]},
        
        # Budget Android
        {"name": "Xiaomi Redmi Note 13", "price": 1200, "rating": 4.1, "features": ["large battery", "budget friendly", "Android", "value"]},
        {"name": "Samsung Galaxy A35", "price": 1600, "rating": 4.0, "features": ["reliable", "decent specs", "Android", "affordable"]},
        {"name": "Motorola Edge 40", "price": 1800, "rating": 4.1, "features": ["clean Android", "good design", "near stock", "affordable"]},
        {"name": "Nothing Phone 2a", "price": 1400, "rating": 4.0, "features": ["unique design", "clean software", "Android", "distinctive"]},
        {"name": "OPPO Reno 11", "price": 1600, "rating": 3.9, "features": ["good selfie", "decent performance", "Android", "mid-budget"]},
        {"name": "Vivo V30", "price": 1800, "rating": 4.0, "features": ["camera focused", "good design", "Android", "photography"]}
    ],
    "laptops": [
        # macOS Laptops
        {"name": "MacBook Pro 16 M3 Max", "price": 12000, "rating": 4.9, "features": ["M3 Max chip", "macOS", "creative work", "premium"]},
        {"name": "MacBook Pro 14 M3 Pro", "price": 9500, "rating": 4.8, "features": ["M3 Pro chip", "macOS", "professional", "portable"]},
        {"name": "MacBook Pro 13 M3", "price": 8500, "rating": 4.7, "features": ["M3 chip", "macOS", "compact pro", "reliable"]},
        {"name": "MacBook Air 15 M3", "price": 6800, "rating": 4.6, "features": ["large screen", "M3 chip", "macOS", "thin light"]},
        {"name": "MacBook Air 13 M3", "price": 5800, "rating": 4.5, "features": ["ultra portable", "M3 chip", "macOS", "everyday"]},
        {"name": "MacBook Air 13 M2", "price": 4800, "rating": 4.4, "features": ["proven performance", "M2 chip", "macOS", "reliable"]},
        {"name": "MacBook Air 13 M1", "price": 3800, "rating": 4.3, "features": ["great value", "M1 chip", "macOS", "efficient"]},
        
        # Windows Premium
        {"name": "Dell XPS 17", "price": 8800, "rating": 4.7, "features": ["4K display", "Intel i7", "Windows", "creative work"]},
        {"name": "Dell XPS 15", "price": 7200, "rating": 4.6, "features": ["premium build", "good display", "Windows", "professional"]},
        {"name": "Dell XPS 13 Plus", "price": 5500, "rating": 4.5, "features": ["compact premium", "modern design", "Windows", "business"]},
        {"name": "Microsoft Surface Laptop 5", "price": 6200, "rating": 4.4, "features": ["touchscreen", "premium feel", "Windows", "versatile"]},
        {"name": "HP Spectre x360 16", "price": 7800, "rating": 4.5, "features": ["2-in-1 design", "OLED option", "Windows", "convertible"]},
        {"name": "Lenovo ThinkPad X1 Carbon", "price": 7500, "rating": 4.6, "features": ["business grade", "lightweight", "Windows", "durable"]},
        
        # Gaming Windows
        {"name": "ASUS ROG Strix G18", "price": 9200, "rating": 4.7, "features": ["RTX 4080", "gaming beast", "Windows", "RGB lighting"]},
        {"name": "MSI Raider GE78", "price": 8600, "rating": 4.6, "features": ["high refresh", "powerful GPU", "Windows", "gaming"]},
        {"name": "Alienware M16", "price": 9800, "rating": 4.8, "features": ["premium gaming", "great cooling", "Windows", "enthusiast"]},
        {"name": "ASUS ROG Zephyrus G14", "price": 6800, "rating": 4.7, "features": ["compact gaming", "good battery", "Windows", "portable"]},
        {"name": "HP Omen 16", "price": 4800, "rating": 4.3, "features": ["affordable gaming", "decent specs", "Windows", "value gaming"]},
        
        # Budget Windows
        {"name": "HP Pavilion 15", "price": 3200, "rating": 4.2, "features": ["budget friendly", "general use", "Windows", "student"]},
        {"name": "Acer Aspire 5", "price": 2800, "rating": 4.0, "features": ["basic tasks", "affordable", "Windows", "entry level"]},
        {"name": "Lenovo IdeaPad 3", "price": 2600, "rating": 3.9, "features": ["everyday computing", "budget option", "Windows", "basic"]},
        {"name": "ASUS VivoBook 15", "price": 3000, "rating": 4.1, "features": ["good value", "decent performance", "Windows", "mainstream"]},
        
        # Linux Laptops
        {"name": "System76 Oryx Pro", "price": 7800, "rating": 4.5, "features": ["Linux native", "developer focused", "Ubuntu", "open source"]},
        {"name": "Dell XPS 13 Developer", "price": 5800, "rating": 4.4, "features": ["Ubuntu certified", "developer edition", "Linux", "premium"]},
        {"name": "Lenovo ThinkPad P1 Linux", "price": 8200, "rating": 4.6, "features": ["workstation grade", "Linux certified", "professional", "powerful"]},
        {"name": "Framework Laptop 13", "price": 4500, "rating": 4.2, "features": ["modular design", "Linux support", "repairable", "innovative"]},
        {"name": "Tuxedo InfinityBook Pro", "price": 5200, "rating": 4.3, "features": ["Linux optimized", "German engineering", "customizable", "developer"]}
    ]
}

def generate_response(messages: List[Dict]) -> str:
    f"""Call {model} API to get shopping advice response"""
    print("\n🤔 Shopping assistant is thinking...\n")
    
    try:
        # # OpenAI connection
        response = client.chat.completions.create(
            messages=messages,
            max_tokens=1024,
            temperature=0.7,  # Slightly creative but focused
            model=model
        )
        # # Deepseek connection
        # response = client.complete(
        #     messages=[
        #         UserMessage(messages),
        #     ],
        #     max_tokens=1000,
        #     model=model
        # )
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"❌ Error calling {model} API: \n{str(e)}\n")
        # Fallback response
        return f'''Sorry, I'm having trouble connecting right now. Let me help with basic product search.

```action
{
    "tool_name": "search_products",
    "args": {"category": "phones"}
}
```'''

def parse_action(response: str) -> Dict:
    """Parse action from shopping assistant response"""
    try:
        if "```action" in response:
            start = response.find("```action") + len("```action")
            end = response.find("```", start)
            action_str = response[start:end].strip()
            action = json.loads(action_str)
            return action
        else:
            return {
                "tool_name": "chat_only",
                "args": {"message": "No specific action needed"}
            }
    except Exception as e:
        return {
            "tool_name": "error",
            "args": {"message": f"Could not understand the request: {str(e)}"}
        }

def get_all_products(category: str):
    """Search products by category and budget"""
    products = PRODUCT_DATABASE.get(category.lower(), [])
    return products


def search_products(category: str, max_price: int = None) -> List[Dict]:
    """Search products by category and budget"""
    products = PRODUCT_DATABASE.get(category.lower(), [])
    
    if max_price:
        products = [p for p in products if p["price"] <= max_price]
    
    # Sort by rating (best first)
    products.sort(key=lambda x: x["rating"], reverse=True)
    return products

def get_product_details(product_name: str) -> Dict:
    """Get detailed info about a specific product"""
    for category in PRODUCT_DATABASE.values():
        for product in category:
            if product_name.lower() in product["name"].lower():
                return {
                    "found": True,
                    "details": product,
                    "category": "phone" if product in PRODUCT_DATABASE["phones"] else "laptop"
                }
    
    return {"found": False, "message": f"Product '{product_name}' not found"}

def compare_products(product1: str, product2: str) -> Dict:
    """Compare two products side by side"""
    p1 = get_product_details(product1)
    p2 = get_product_details(product2)
    
    if not p1["found"] or not p2["found"]:
        return {"error": "One or both products not found"}
    
    return {
        "comparison": {
            "product1": p1["details"],
            "product2": p2["details"],
            "price_difference": abs(p1["details"]["price"] - p2["details"]["price"]),
            "better_rating": p1["details"]["name"] if p1["details"]["rating"] > p2["details"]["rating"] else p2["details"]["name"]
        }
    }

def check_budget_fit(budget: int, category: str = None) -> Dict:
    """Check what products fit within budget"""
    fitting_products = []
    
    search_categories = [category] if category else PRODUCT_DATABASE.keys()
    
    for cat in search_categories:
        if cat in PRODUCT_DATABASE:
            for product in PRODUCT_DATABASE[cat]:
                if product["price"] <= budget:
                    product_copy = product.copy()
                    product_copy["category"] = cat
                    fitting_products.append(product_copy)
    
    # Sort by best value (rating/price ratio)
    fitting_products.sort(key=lambda x: x["rating"]/x["price"]*1000, reverse=True)
    
    return {
        "budget": budget,
        "products_found": len(fitting_products),
        "recommendations": fitting_products[:3],  # Top 3 recommendations
        "savings": budget - fitting_products[0]["price"] if fitting_products else 0
    }

def run_shopping_agent():
    """Main shopping assistant agent loop"""
    
    # Shopping agent rules
    agent_rules = [{
        "role": "system",
        "content": """
You are a helpful shopping assistant that helps customers find the best products based on what user request using this tools (function), without user mention what function / tools. You need to understand what user need and use this tools to response.

Available tools:
- search_products(category: str, max_price: int) -> Find products by category and budget
- get_product_details(product_name: str) -> Get detailed info about a specific product  
- compare_products(product1: str, product2: str) -> Compare two products
- check_budget_fit(budget: int, category: str) -> Find products within budget
- recommend_best() -> Give final recommendation based on conversation
- terminate(message: str) -> If user want or act = End conversation with summary

Categories available: "phones", "laptops"

Always try to understand the customer's:
1. Budget range
2. Intended use (gaming, work, casual, etc.)
3. Preferences (brand, features, etc.)

Respond in this format when you want to use a tool:

```action
{
    "tool_name": "tool_name_here",
    "args": {"param": "value"}
}
```

If just chatting/asking questions, no action block needed.
Be friendly and helpful! Ask clarifying questions when needed.
"""
    }]

    print("=== SMART SHOPPING ASSISTANT ===")
    print("Helping you find the perfect product!")
    print("-" * 50)

    # Initialize conversation
    user_input = input("\n🗣️ You: ").strip()
    
    if not user_input:
        user_input = "Hi, I need help choosing a product"
    
    # Initialize conversation with user's actual input
    memory = [
        {"role": "user", "content": user_input}
    ]

    max_iterations = 22
    iterations = 0

    # The Shopping Agent Loop
    while iterations < max_iterations:
        print(f"\n--- CONVERSATION TURN {iterations + 1} ---")
        
        # 1. Prepare prompt with agent rules + conversation history
        prompt = agent_rules + memory

        # 2. Get shopping advice from AI
        response = generate_response(prompt)
        print(f"🛒 Shopping Assistant: {response}")

        # 3. Parse any actions
        action = parse_action(response)
        print(f"\n🔧 Action to take: {action}")

        # 4. Execute shopping tools
        result = {"status": "no action needed"}

        if action["tool_name"] == "search_products":
            products = search_products(
                action["args"]["category"], 
                action["args"]["max_price"]
            )
            result = {"products": products}
            print(f"\n🔍 Found {len(products)} products in {action['args']['category']}")
            
        elif action["tool_name"] == "get_product_details":
            details = get_product_details(action["args"]["product_name"])
            result = details
            print(f"\n📱 Product details retrieved")
            
        elif action["tool_name"] == "compare_products":
            comparison = compare_products(
                action["args"]["product1"],
                action["args"]["product2"]
            )
            result = comparison
            print(f"\n⚖️ Compared products")
            
        elif action["tool_name"] == "check_budget_fit":
            budget_analysis = check_budget_fit(
                action["args"]["budget"],
                action["args"]["category"]
            )
            result = budget_analysis
            print(f"\n💰 Checked budget fit: {budget_analysis['products_found']} options found")

        elif action["tool_name"] == "recommend_best":
            result = {"message": "Based on our conversation, here are my final recommendations"}
            print("\n🎯 Providing final recommendations")

        elif action["tool_name"] == "terminate":
            print(f"✅ Shopping session completed: {action['args']['message']}")
            break
            
        elif action["tool_name"] == "chat_only":
            result = {"message": "Continuing conversation, no tools needed"}
            
        elif action["tool_name"] == "error":
            result = {"error": action["args"]["message"]}
            print(f"❌ Error: {result['error']}")

        print(f"\n📊 Tool result: {json.dumps(result, indent=2)}")

        # 5. Update conversation memory
        memory.extend([
            {"role": "assistant", "content": response},
            {"role": "user", "content": json.dumps(result)}
        ])

        # 6. Get next user input (if agent is asking questions)
        if action["tool_name"] == "chat_only" and "?" in response:
            print("\n\n" + "="*40)
            next_input = input("🗣️ You: ").strip()
            if next_input:
                # Replace the tool result with actual user input
                memory[-1] = {"role": "user", "content": next_input}
                print(f"📝 Updated conversation with your input: {next_input}")

        # 7. Check if conversation should continue
        if action["tool_name"] == "terminate":
            break

        iterations += 1

    # Show final summary
    print(f"\n🏁 Shopping consultation completed!")
    print(f"Total conversation turns: {iterations}")
    print("Thank you for using Smart Shopping Assistant! 🛍️")

# Demo function to show individual tools
def demo_shopping_tools():
    print("\n" + "="*50)
    print("DEMO: Shopping Tools")
    print("="*50)

    # product = get_all_products("phones")

    # print("\n1. 🔍 Search phones under RM3000:")
    # phones = search_products("phones", 3000)
    # for phone in phones:
    #     print(f"   - {phone['name']}: RM{phone['price']} (⭐{phone['rating']})")
    
    # print("\n2. 📱 Get iPhone 15 details:")
    # details = get_product_details("iPhone 15")
    # if details["found"]:
    #     product = details["details"]
    #     print(f"   - {product['name']}: RM{product['price']}")
    #     print(f"   - Rating: ⭐{product['rating']}")
    #     print(f"   - Features: {', '.join(product['features'])}")
    
    # print("\n3. ⚖️ Compare iPhone SE vs Xiaomi 14:")
    # comparison = compare_products("iPhone SE", "Xiaomi 14")
    # if "comparison" in comparison:
    #     comp = comparison["comparison"]
    #     print(f"   - Price difference: RM{comp['price_difference']}")
    #     print(f"   - Better rating: {comp['better_rating']}")
    
    # print("\n4. 💰 Check RM2500 budget:")
    # budget_check = check_budget_fit(2500)
    # print(f"   - Found {budget_check['products_found']} products")
    # print(f"   - Top recommendation: {budget_check['recommendations'][0]['name'] if budget_check['recommendations'] else 'None'}")

if __name__ == "__main__":
    # Demo individual tools first
    demo_shopping_tools()
    
    print("\n" + "="*50)
    print("Starting Shopping Assistant Agent Loop...")
    print("="*50)
    
    # Run the main shopping agent
    run_shopping_agent()