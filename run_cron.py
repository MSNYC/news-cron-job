import os
import time
import urllib.error
import urllib.request

# Load configuration from environment variables so nothing sensitive is stored in git.
API_KEY = os.getenv('MY_SECRET_API_KEY')
VERCEL_URL = os.getenv(
    'VERCEL_URL',
    'https://news-monitor-five.vercel.app/api/send-news',
)
MAX_RETRIES = 3
TIMEOUT_SECONDS = 120
RETRY_DELAY_SECONDS = 30

def send_request():
    if not API_KEY:
        print("Missing required MY_SECRET_API_KEY secret.")
        return False

    request = urllib.request.Request(
        VERCEL_URL,
        headers={"X-API-KEY": API_KEY},
        method="GET",
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"Attempt {attempt}/{MAX_RETRIES}: Sending request to {VERCEL_URL}")
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                status_code = response.getcode()

            if status_code == 200:
                print("News email triggered successfully!")
                return True
            print(f"Request failed with status code {status_code}.")

        except TimeoutError:
            print(f"Attempt {attempt} timed out after {TIMEOUT_SECONDS} seconds.")
        except urllib.error.HTTPError as error:
            print(f"Attempt {attempt} failed with HTTP {error.code}.")
        except urllib.error.URLError as error:
            print(f"Attempt {attempt} connection error: {error.reason}")
        except Exception as error:
            print(f"Attempt {attempt} unexpected error: {error}")

        if attempt < MAX_RETRIES:
            print(f"Waiting {RETRY_DELAY_SECONDS} seconds before retry...")
            time.sleep(RETRY_DELAY_SECONDS)

    print(
        f"All {MAX_RETRIES} attempts failed. "
        "The endpoint may be down or taking too long to respond."
    )
    return False

if __name__ == "__main__":
    success = send_request()
    exit(0 if success else 1)
