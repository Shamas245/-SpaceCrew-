# test_config_and_tools.py
from agent.config import Config
from agent.tools.api_tools import APITools

def test_config():
    print("Testing Config...")
    print(f"NASA API Key exists: {'NASA_API_KEY' in Config.__dict__}")
    print(f"OpenAI API Key exists: {'OPENAI_API_KEY' in Config.__dict__}")

def test_api_tools():
    print("\nTesting API Tools...")
    try:
        # Test OpenNotify API (doesn't require API key)
        print("Testing Open Notify API...")
        data = APITools.fetch_open_notify_data("astros.json")
        print("✓ Open Notify API works!")
        print(f"Current astronauts in space: {data['number']}")
    except Exception as e:
        print(f"✗ Open Notify API failed: {str(e)}")

    try:
        # Test NASA APOD
        print("\nTesting NASA APOD API...")
        data = APITools.fetch_nasa_apod()
        print("✓ NASA APOD API works!")
        print(f"Today's astronomy picture title: {data.get('title')}")
    except Exception as e:
        print(f"✗ NASA APOD API failed: {str(e)}")

if __name__ == "__main__":
    test_config()
    test_api_tools()