import os
import requests
from dotenv import load_dotenv

# Load environment from .env 
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

API_USER = os.getenv("API_USER")
API_SECRET = os.getenv("API_SECRET")

def analyze_sightengine(image_path):
    try:
        if not API_USER or not API_SECRET:
            raise ValueError("API credentials not found. Check .env file.")

        with open(image_path, 'rb') as image_file:
            files = {'media': image_file}
            data = {
                'models': 'genai',
                'api_user': API_USER,
                'api_secret': API_SECRET
            }

            response = requests.post(
                'https://api.sightengine.com/1.0/check.json',
                files=files,
                data=data
            )
            response.raise_for_status()
            json_data = response.json()

            # Debug log of full response
            print("[SightEngine] Raw Response:", json_data)

            # Return actual score from correct path
            return float(json_data.get("type", {}).get("ai_generated", 0.0))

    except Exception as e:
        print("[ERROR] SightEngine request failed:", e)
        return 0.0
