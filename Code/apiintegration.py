import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API credentials from the .env file
API_USER = os.getenv("API_USER")
API_SECRET = os.getenv("API_SECRET")

params = {
    'models': 'genai',  # Ensure this is correctly formatted
    'api_user': API_USER,  
    'api_secret': API_SECRET
}

# Correct file path for Windows
file_path = r"E:\Uni\grad project\traiced\image_files\DallEOTGJ\FruitsDallE10.jpg"

try:
    with open(file_path, 'rb') as file:
        files = {'media': file}
        r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
        output = json.loads(r.text)
        print(json.dumps(output, indent=4))
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
