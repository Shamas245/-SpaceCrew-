# data_fetcher.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from agent.tools.api_tools import APITools
from agent.config import Config
import json

class DataFetcher:
    def __init__(self):
        self.client = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=Config.GEMINI_API_KEY
        )
        self.api_tools = APITools()

    def fetch(self, endpoint: str, parameters: dict) -> dict:
        # Map endpoint names to their correct API methods
        endpoint_mapping = {
            "current_astronauts": ("astros", self.api_tools.fetch_open_notify_data),
            "iss_location": ("iss-now", self.api_tools.fetch_open_notify_data),
            "apod": ("apod", self.api_tools.fetch_nasa_apod),
            "astronaut_info": ("astronaut", self.api_tools.fetch_launch_library_data)
        }

        if endpoint not in endpoint_mapping:
            return {"error": f"Unknown endpoint: {endpoint}"}

        api_endpoint, fetch_method = endpoint_mapping[endpoint]
        
        # Get API response
        try:
            if endpoint == "apod":
                data = fetch_method()
            elif endpoint == "astronaut_info":
                data = fetch_method(api_endpoint, parameters)
            else:
                data = fetch_method(api_endpoint)

            # Check for error in response
            if isinstance(data, dict) and "error" in data:
                return data

            # Create validation prompt
            system_message = SystemMessage(content=[{
                "type": "text",
                "text": """You are a data validation specialist. Analyze the provided API response 
                and return ONLY 'VALID' if the data is complete and well-formed, or describe specific 
                issues if you find any problems. Be concise."""
            }])

            human_message = HumanMessage(content=[{
                "type": "text",
                "text": f"Validate this {endpoint} response:\n{json.dumps(data, indent=2)}"
            }])

            # Get validation response
            validation_response = self.client.invoke([system_message, human_message])
            validation_text = validation_response.content

            # Only consider it an error if specific issues are found
            if validation_text.strip().upper() != "VALID" and "VALID" not in validation_text.upper():
                return {
                    "error": "Validation failed",
                    "details": validation_text,
                    "data": data
                }

            return data

        except Exception as e:
            return {"error": f"Error processing request: {str(e)}"}
        