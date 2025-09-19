import json
import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GAMETravelAgent:
    def __init__(self):
        # Initialize API client with configuration
        self.token = os.getenv("QWEN_3_API_KEY")
        self.model = "qwen/qwen3-coder:free"  # Fixed: removed comma
        self.endpoint = "https://openrouter.ai/api/v1"
        
        self.client = OpenAI( 
            base_url=self.endpoint,
            api_key=self.token,
        )
        
        # GOAL: Help user plan a complete trip
        self.goal = "Help user plan a comprehensive travel itinerary"
        
        # MEMORY: Store conversation history and user preferences
        self.memory = {
            "conversation_history": [],
            "user_preferences": {},
            "trip_details": {}
        }
        
        # ACTIONS: Available tools/functions
        self.actions = {
            "search_flights": self.search_flights,
            "find_hotels": self.find_hotels,
            "get_attractions": self.get_attractions,
            "check_weather": self.check_weather,
            "create_itinerary": self.create_itinerary
        }
        
        # ENVIRONMENT: External APIs and services
        self.environment_apis = {
            "flight_api": "https://api.flightservice.com",
            "hotel_api": "https://api.hotelservice.com",
            "weather_api": "https://api.weatherservice.com"
        }

    def generate_response(self, messages: List[Dict]) -> str:  # Fixed: added self parameter
        """Call LLM API to get response"""
        print("\n🤔 LLM is thinking...\n")
        
        try:
            response = self.client.chat.completions.create(  # Fixed: use self.client
                messages=messages,
                max_tokens=1024,
                temperature=0.7,
                model=self.model  # Fixed: use self.model
            )
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"❌ Error calling {self.model} API: \n{str(e)}\n")  # Fixed: use self.model
            return "Sorry, I'm having trouble connecting right now."

    def search_flights(self, origin: str, destination: str, date: str):
        """Simulate flight search API call"""
        print(f"🔍 Searching flights from {origin} to {destination} on {date}")
        # In real implementation, this would call actual flight API
        return f"Found 3 flights from {origin} to {destination} on {date}: Economy from $200"

    def find_hotels(self, destination: str, check_in: str, check_out: str, budget: int):
        """Simulate hotel search API call"""
        print(f"🏨 Finding hotels in {destination} for ${budget}/night")
        return f"Found 5 hotels in {destination} within budget: 3-star from $80/night"

    def get_attractions(self, destination: str):
        """Simulate attractions API call"""
        print(f"🏛️ Getting attractions for {destination}")
        return f"Top attractions in {destination}: Museum, Beach, Historic Sites"

    def check_weather(self, destination: str, date: str):
        """Simulate weather API call"""
        print(f"🌤️ Checking weather in {destination} on {date}")
        return f"Weather in {destination} on {date}: Sunny, 25°C"

    def create_itinerary(self, details: dict):
        """Create final itinerary"""
        print("📅 Creating comprehensive itinerary")
        return f"""Complete Itinerary for {details['destination']}:
        - Flights: {details.get('flights', 'To be booked')}
        - Hotels: {details.get('hotels', 'To be booked')}
        - Activities: {details.get('activities', 'To be planned')}
        """

    def process_user_input(self, user_input: str):
        """Main GAME loop processing"""
        # Add to memory
        self.memory["conversation_history"].append({"role": "user", "content": user_input})
        
        # Prepare context for LLM
        system_prompt = f"""You are a travel planning assistant. Your goal: {self.goal}

Available actions:
- search_flights(origin, destination, date)
- find_hotels(destination, check_in, check_out, budget)  
- get_attractions(destination)
- check_weather(destination, date)
- create_itinerary(details)

Current memory:
{json.dumps(self.memory, indent=2)}

Respond with JSON containing:
- "response": Natural language response to user
- "action": {{"name": "action_name", "args": {{arg: value}}}} (optional)
- "update_memory": {{memory updates}} (optional)
"""

        messages = [
            {"role": "system", "content": system_prompt},
            *self.memory["conversation_history"]
        ]
        print(f"🧠 System Prompt: {messages}")
        
        # Get LLM response
        llm_response = self.generate_response(messages)
        print(f"🤖 LLM Response: {llm_response}")
        
        try:
            # Parse LLM response (assuming JSON format)
            response_data = json.loads(llm_response)
            
            # Execute action if specified
            if "action" in response_data:
                action_name = response_data["action"]["name"]
                action_args = response_data["action"]["args"]
                
                if action_name in self.actions:
                    action_result = self.actions[action_name](**action_args)
                    response_data["response"] += f"\n\nAction Result: {action_result}"
            
            # Update memory if specified
            if "update_memory" in response_data:
                self.memory.update(response_data["update_memory"])
            
            # Add to conversation history
            self.memory["conversation_history"].append({
                "role": "assistant", 
                "content": response_data["response"]
            })
            
            return response_data["response"]
            
        except json.JSONDecodeError:
            # Fallback if LLM doesn't return JSON
            self.memory["conversation_history"].append({
                "role": "assistant", 
                "content": llm_response
            })
            return llm_response

# Example usage
if __name__ == "__main__":
    agent = GAMETravelAgent()
    
    # Simulated conversation
    user_inputs = [
        "I want to plan a trip to Bali next month",
        "My budget is $1500 and I'm traveling from Singapore",
        "I'll be there from June 15-20, 2024"
    ]
    
    for user_input in user_inputs:
        print(f"\n👤 User: {user_input}")
        response = agent.process_user_input(user_input)
        print(f"🤖 Agent: {response}")