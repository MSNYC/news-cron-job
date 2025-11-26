import requests
import os
import time

# Load API key from environment variables (to avoid hardcoding it in the script)
API_KEY = os.getenv('MY_SECRET_API_KEY')
VERCEL_URL = "https://news-monitor-five.vercel.app/api/send-news"  # Your Vercel endpoint

def send_request():
    headers = {"X-API-KEY": API_KEY}

    # Retry logic to handle Render free tier spin-up time
    max_retries = 3
    timeout = 120  # 2 minutes timeout to allow service to wake up

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt}/{max_retries}: Sending request to {VERCEL_URL}")
            response = requests.get(VERCEL_URL, headers=headers, timeout=timeout)

            if response.status_code == 200:
                print("News email triggered successfully!")
                return True
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            print(f"Attempt {attempt} timed out after {timeout} seconds")
            if attempt < max_retries:
                wait_time = 30
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)

        except requests.exceptions.ConnectionError as e:
            print(f"Attempt {attempt} connection error: {str(e)}")
            if attempt < max_retries:
                wait_time = 30
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)

        except Exception as e:
            print(f"Attempt {attempt} unexpected error: {str(e)}")
            if attempt < max_retries:
                wait_time = 30
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)

    print(f"All {max_retries} attempts failed. The Render service may be down or taking too long to wake up.")
    return False

if __name__ == "__main__":
    success = send_request()
    exit(0 if success else 1)
