from litellm import completion
import os

# Set ENV variables
os.environ["GOOGLE_API_KEY"] = "AIzaSyAx5uJueg89ueR6G41Jhcqsy1mBDKOfGv8"  # Use GOOGLE_API_KEY instead of GEMINI_API_KEY

def factory():
    try:
        response = completion(
            model="gemini-1.5-flash",  # Correct model name format
            messages=[{
                "role": "user",
                "content": "Hello, how are you?"
            }]
        )
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test the function
if __name__ == "__main__":
    result = factory()
    print(result)