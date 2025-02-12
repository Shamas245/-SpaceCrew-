from langchain_google_genai import ChatGoogleGenerativeAI
from agent.tools.api_tools import APITools
from agent.config import Config
from langchain_core.messages import HumanMessage, SystemMessage
import json

class QueryAnalyzer:
    def __init__(self):
        self.client = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=Config.GEMINI_API_KEY
        )
    
    def analyze(self, query: str, conversation_context: str = "") -> dict:
        # System message content
        system_content = """You are an expert at analyzing space-related queries and determining 
        which NASA or space API would be most appropriate to answer the question. You analyze
        queries and return a JSON response specifying the most suitable API endpoint.
        
        You must ALWAYS return your response in valid JSON format.
        
        Example response format:
        {
            "endpoint": "current_astronauts",
            "parameters": {}
        }"""
        
        # Human message content
        human_content = f"""Analyze this space-related query: '{query}'
        
        Previous conversation context:
        {conversation_context}
        
        Available API endpoints:
        - astronaut_info (Launch Library API)
        - current_astronauts (Open Notify API)
        - apod (NASA APOD API)
        - iss_location (Open Notify API)
        
        Return ONLY a JSON object with 'endpoint' and 'parameters' fields.
        The response must be valid JSON.
        """
        
        try:
            # Create messages - note we're simplifying the content structure
            messages = [
                SystemMessage(content=system_content),
                HumanMessage(content=human_content)
            ]
            
            # Invoke the model
            response = self.client.invoke(messages)
            
            # Get the response content - this might vary based on the actual response structure
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Print for debugging
            print(f"Raw response: {response_text}")
            
            # Try to clean the response if it contains markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse and return the JSON response
            parsed_response = json.loads(response_text)
            
            # Ensure the response has the required fields
            if "endpoint" not in parsed_response:
                raise ValueError("Response missing 'endpoint' field")
            
            return parsed_response
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text}")
            # Return a default response instead of raising an error
            return {
                "endpoint": "error",
                "parameters": {"error": "Failed to parse response"},
                "original_response": response_text
            }
        except Exception as e:
            print(f"Error during analysis: {e}")
            return {
                "endpoint": "error",
                "parameters": {"error": str(e)}
            }