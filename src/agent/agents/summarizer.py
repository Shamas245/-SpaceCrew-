# src/space_agent/agents/summarizer.py
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.config import Config
from langchain_core.messages import HumanMessage, SystemMessage

class Summarizer:
    def __init__(self):
        self.client = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=Config.GEMINI_API_KEY
        )

    def summarize(self, data: dict, user_type: str, query: str, conversation_context: str = "") -> str:
        # System message content
        system_content = {
            "type": "text",
            "text": f"""You are an expert at creating {user_type}-friendly summaries of 
            space-related information. You consider previous conversation context to provide more 
            relevant and connected responses."""
        }
        
        # User message content
        user_content = {
            "type": "text",
            "text": f"""
            Create a {user_type}-friendly summary of this space data.
            Original query: {query}
            
            Previous conversation context:
            {conversation_context}
            
            Data to summarize:
            {data}
            
            Ensure the summary:
            - Is appropriate for the user type ({user_type})
            - References relevant information from previous conversation when appropriate
            - Is well-structured and clear
            - Is accurate to the source data
            - Is engaging and informative
            - Maintains continuity with previous responses when relevant
            """
        }

        try:
            # Create messages using the LangChain structure
            messages = [
                SystemMessage(content=[system_content]),
                HumanMessage(content=[user_content])
            ]
            
            # Invoke the model with the messages
            response = self.client.invoke(messages)
            
            # Get the response content
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
                
        except Exception as e:
            print(f"Error during summarization: {e}")
            return f"Error generating summary: {str(e)}"