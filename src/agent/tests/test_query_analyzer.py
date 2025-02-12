# test_query_analyzer.py
from agent.agents.query_analyzer import QueryAnalyzer

def test_query_analyzer():
    print("Testing Query Analyzer...")
    analyzer = QueryAnalyzer()
    
    # Test different types of queries
    test_queries = [
        "Who are the current astronauts in space?",
        "Show me today's astronomy picture",
        "Tell me about astronaut Neil Armstrong"
    ]
    
    for query in test_queries:
        print(f"\nTesting query: {query}")
        try:
            result = analyzer.analyze(query)
            print(f"✓ Analysis successful!")
            print(f"Result: {result}")
        except Exception as e:
            print(f"✗ Analysis failed: {str(e)}")

if __name__ == "__main__":
    test_query_analyzer()