# test_data_fetcher.py

from agent.agents.data_fetcher import DataFetcher
import json

def test_data_fetcher():
    """Run tests for the DataFetcher class"""
    print("Running endpoint tests...")
    
    fetcher = DataFetcher()
    
    # Define test cases
    test_cases = [
        ("current_astronauts", {}),
        ("iss_location", {}),
        ("apod", {}),
        ("astronaut_info", {"name": "Neil Armstrong"})
    ]
    
    print("\nTest Results Summary:")
    print("=" * 50)
    
    results = {}
    for endpoint, params in test_cases:
        print(f"\nTesting endpoint: {endpoint}")
        try:
            result = fetcher.fetch(endpoint, params)
            success = "error" not in result
            
            if success:
                print(f"✓ Success!")
                # Truncate long responses for readability
                truncated_result = json.dumps(result, indent=2)[:200] + "..."
                print(f"Sample data: {truncated_result}")
            else:
                print(f"✗ Failed: {result.get('error', 'Unknown error')}")
                if 'details' in result:
                    print(f"Details: {result['details']}")
            
            results[endpoint] = {
                "success": success,
                "result": result
            }
            
        except Exception as e:
            print(f"✗ Failed with exception: {str(e)}")
            results[endpoint] = {
                "success": False,
                "error": str(e)
            }
        
        print("-" * 50)
    
    return results

if __name__ == "__main__":
    test_data_fetcher()