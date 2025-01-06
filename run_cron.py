import requests
import os

# Load API key from environment variables (to avoid hardcoding it in the script)
API_KEY = os.getenv('MY_SECRET_API_KEY')
RENDER_URL = "https://newsmonitor.onrender.com/"  # Your Render endpoint

def send_request():
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(RENDER_URL, headers=headers)
    if response.status_code == 200:
        print("News email triggered successfully!")
    else:
        print(f"Failed to trigger news email. Status Code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    send_request()
