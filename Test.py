import requests

# The URL where your Docker container is listening
url = 'http://localhost:9696/predict'

# The player data to send
player = {
    "age": 22,
    "npxg+xag": 8.5,
    "starts": 25,
    "team": "Arsenal", 
    "pos": "Forward"
}

print(f"Sending player data to {url}...")

# Send the request
try:
    response = requests.post(url, json=player).json()
    print("\n--- Prediction Success ---")
    print(response)
except requests.exceptions.ConnectionError:
    print("\n Error: Could not connect to the server.")
    print("Make sure your Docker container is running!")