# test_summarizer.py
from agent.agents.summarizer import Summarizer

def test_summarizer():
    print("Testing Summarizer...")
    summarizer = Summarizer()
    
    # Test data to summarize
    test_data = {
        "number": 7,
        "people": [
            {"name": "Astronaut 1", "craft": "ISS"},
            {"name": "Astronaut 2", "craft": "ISS"}
        ]
    }
    
    # Test for different user types
    user_types = ["student", "teacher", "researcher"]
    
    for user_type in user_types:
        print(f"\nTesting summary for {user_type}")
        try:
            result = summarizer.summarize(
                test_data,
                user_type,
                "Who is currently in space?"
            )
            print(f"✓ Summarization successful!")
            print(f"Result: {result}")
        except Exception as e:
            print(f"✗ Summarization failed: {str(e)}")

if __name__ == "__main__":
    test_summarizer()