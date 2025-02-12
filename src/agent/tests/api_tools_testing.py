from agent.tools.api_tools import APITools
import json

def test_endpoints(self):
        """Test method to verify all endpoints are working"""
        test_cases = [
            ("current_astronauts", {}),
            ("iss_location", {}),
            ("apod", {}),
            ("astronaut_info", {"name": "Neil Armstrong"})
        ]
        
        results = {}
        print("\nTest Results Summary:")
        print("=" * 50)
        
        for endpoint, params in test_cases:
            print(f"\nTesting endpoint: {endpoint}")
            try:
                result = self.fetch(endpoint, params)
                success = "error" not in result
                
                # Format the result for display
                if success:
                    print(f"✓ Success!")
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