import requests
from ..config import Config

class APITools:
    def __init__(self):
        # Store base URLs as instance variables for easier access
        self.launch_library_base_url = "http://api.open-notify.org"  # Example URL, replace with actual
        self.open_notify_base_url = "http://api.open-notify.org"
        self.nasa_base_url = "https://api.nasa.gov/planetary"
        
    def fetch_nasa_apod(self) -> dict:
        """Fetch Astronomy Picture of the Day from NASA API"""
        url = f"{self.nasa_base_url}/apod"
        params = {
            "api_key": Config.NASA_API_KEY
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch NASA APOD: {str(e)}"}
            
    def fetch_launch_library_data(self, endpoint: str, parameters: dict) -> dict:
        """Fetch data from Launch Library API"""
        url = f"{self.launch_library_base_url}/{endpoint}"
        try:
            response = requests.get(url, params=parameters)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch data from Launch Library: {str(e)}"}
            
    def fetch_open_notify_data(self, endpoint: str) -> dict:
        """Fetch data from Open Notify API"""
        url = f"{self.open_notify_base_url}/{endpoint}.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch data from Open Notify: {str(e)}"}
            
    def test_endpoints(self) -> dict:
        """Test all API endpoints"""
        results = {}
        
        # Test NASA APOD
        print("\nTesting NASA APOD endpoint...")
        try:
            apod_result = self.fetch_nasa_apod()
            results["nasa_apod"] = {
                "success": "error" not in apod_result,
                "data": apod_result
            }
        except Exception as e:
            results["nasa_apod"] = {
                "success": False,
                "error": str(e)
            }
        
        # Test Open Notify endpoints
        open_notify_endpoints = ["iss-now", "astros"]
        for endpoint in open_notify_endpoints:
            print(f"\nTesting Open Notify endpoint: {endpoint}")
            try:
                result = self.fetch_open_notify_data(endpoint)
                results[endpoint] = {
                    "success": "error" not in result,
                    "data": result
                }
            except Exception as e:
                results[endpoint] = {
                    "success": False,
                    "error": str(e)
                }
        
        return results