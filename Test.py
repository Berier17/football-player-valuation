import requests

# 1. Your new Cloud URL
host = "https://valuation-api-300316357465.us-central1.run.app"
url = f"{host}/predict"

# 2. Player data
player = {
    "age": 22,
    "npxg+xag": 8.5,
    "starts": 25,
    "team": "Arsenal", 
    "pos": "Forward"
}

print(f"Sending data to Google Cloud: {url}...")

try:
    response = requests.post(url, json=player).json()
    print("\n--- Cloud Prediction Success ---")
    print(response)
except Exception as e:
    print(f"\n Error: {e}")