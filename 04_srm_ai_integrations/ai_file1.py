import requests
import json


# Replace with your actual API key
#INSERT HUGGING FACE API KEY

# The Gemma3-1B API endpoint
API_URL = "https://api.huggingface.co/models/gemma2-2b"  #Example, check the documentation!

def get_data_from_gemma3(api_key):
    """
    Fetches data from the Gemma3-1B API.
    """
    try:
        response = requests.post(API_URL, headers={"Content-Type": "application/json"}, data="Your data here") #Replace with real request.
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None

if __name__ == "__main__":
    data = get_data_from_gemma3(API_KEY)

    if data:
        print("Data from Gemma3-1B:")
        print(data)
    else:
        print("Failed to retrieve data.")
