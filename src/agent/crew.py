from crewai import Task, Crew, Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from agent.tools.api_tools import APITools
from agent.agents.data_fetcher import DataFetcher
from agent.memory.conversation_manager import ConversationManager
import logging
from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpaceCrew:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=Config.GEMINI_API_KEY
        )
        self.api_tools = APITools()
        self.data_fetcher = DataFetcher()
        self.conversation_manager = ConversationManager()
        
    def _create_tools(self):
        """Create properly formatted tools for the agents"""
        
        # NASA APOD Tool
        nasa_apod_tool = Tool(
            name="nasa_apod",
            func=self.api_tools.fetch_nasa_apod,
            description="Fetches NASA's Astronomy Picture of the Day with explanation"
        )
        
        # Open Notify Tools
        open_notify_tool = Tool(
            name="open_notify",
            func=self.api_tools.fetch_open_notify_data,
            description="Fetches data from Open Notify API (ISS location and astronaut information)"
        )
        
        # Launch Library Tool
        launch_library_tool = Tool(
            name="launch_library",
            func=lambda x: self.api_tools.fetch_launch_library_data("astronaut", x),
            description="Fetches astronaut information from the Launch Library"
        )
        
        # Data Fetcher Tool
        data_fetcher_tool = Tool(
            name="data_fetcher",
            func=self.data_fetcher.fetch,
            description="General purpose data fetcher that can retrieve data from various space-related endpoints"
        )
        
        return [nasa_apod_tool, open_notify_tool, launch_library_tool, data_fetcher_tool]

    def create_agents(self):
        """Create specialized agents for the space crew"""
        tools = self._create_tools()
        
        # Query Analysis Agent
        query_analyzer = Agent(
            role='Query Analyzer',
            goal='Analyze user queries to determine appropriate data endpoints and parameters',
            backstory="""You are an expert at understanding space-related questions and 
            determining which NASA or space API endpoints would best answer them. You consider 
            the conversation history to provide context-aware analysis.""",
            tools=[],  # Query analyzer doesn't need tools
            llm=self.llm,
            verbose=True
        )

        # Data Fetcher Agent
        data_fetcher = Agent(
            role='Data Fetcher',
            goal='Fetch and validate space-related data from various APIs',
            backstory="""You are a specialist in retrieving data from NASA and other space 
            APIs. You know how to handle different endpoints and validate the returned data.""",
            tools=tools,  # All tools available to the data fetcher
            llm=self.llm,
            verbose=True
        )

        # Data Summarizer Agent
        data_summarizer = Agent(
            role='Data Summarizer',
            goal='Create clear, contextual summaries of space-related information',
            backstory="""You are an expert at creating engaging and informative summaries 
            of space data. You consider the user's previous questions and knowledge level 
            to provide relevant context.""",
            tools=[],  # Summarizer doesn't need tools
            llm=self.llm,
            verbose=True
        )

        return query_analyzer, data_fetcher, data_summarizer

    def create_tasks(self, query: str, user_type: str = "general"):
        """Create sequential tasks for processing the query"""
        
        context = self.conversation_manager.get_context()
        query_analyzer, data_fetcher, data_summarizer = self.create_agents()

        # Task 1: Analyze Query
        analyze_task = Task(
            description=f"""Analyze this query: '{query}'
            Previous conversation context: {context}
            
            Determine:
            1. Which API endpoint would best answer this query
            2. What parameters are needed for the API call
            3. How this query relates to previous conversation context
            
            Return your analysis as a JSON string with 'endpoint' and 'parameters' keys.""",
            agent=query_analyzer,
            expected_output="A JSON string containing endpoint and parameters for the API call"
        )

        # Task 2: Fetch Data
        fetch_task = Task(
            description="""Using the analysis results:
            1. Select the appropriate tool based on the endpoint
            2. Fetch the data using the provided parameters
            3. Validate the response data
            
            Return the complete, validated data.""",
            agent=data_fetcher,
            dependencies=[analyze_task],
            expected_output="Validated data from the selected API endpoint"
        )

        # Task 3: Summarize Data
        summarize_task = Task(
            description=f"""Create a user-friendly summary of the data:
            User type: {user_type}
            Original query: {query}
            Conversation context: {context}
            
            Make it engaging and informative, explaining any technical terms as needed.""",
            agent=data_summarizer,
            dependencies=[fetch_task],
            expected_output="A user-friendly summary of the space-related data"
        )

        return [analyze_task, fetch_task, summarize_task]

    def process_query(self, query: str, user_type: str = "general") -> str:
        """Process a user query through the crew workflow"""
        try:
            logger.info(f"Processing query: {query} for user type: {user_type}")
            
            tasks = self.create_tasks(query, user_type)
            crew = Crew(
                agents=self.create_agents(),
                tasks=tasks,
                verbose=True
            )

            result = crew.kickoff()
            
            self.conversation_manager.add_to_memory(query, result)
            logger.info("Query processed and saved to conversation history")
            
            return result

        except Exception as e:
            error_msg = f"An error occurred during query processing: {str(e)}"
            logger.error(error_msg)
            return error_msg

def main():
    """Main function to demonstrate the crew's capabilities"""
    crew = SpaceCrew()
    
    test_queries = [
        ("What is today's astronomy picture of the day?", "general")
    ]
    
    for query, user_type in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"User Type: {user_type}")
        print(f"{'='*50}")
        
        result = crew.process_query(query, user_type)
        print(f"\nResponse:\n{result}\n")

if __name__ == "__main__":
    main()
