import requests
from sys import argv
import os

from requests.models import HTTPError

SECRETS_DIR = "./secrets"

try:
    print(f"args: {len(argv)}")
    name = argv[1]
    token = argv[2]
except:
    print("Usage: ./create-princple.py <string:name> <string:access_token>")
    exit(1)


url = "http://localhost:8181/api/management/v1/principals"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
data = {
    "name": f"{name}",
    "type": "user"
}

response = requests.post(url, headers=headers, json=data)

try:
    response.raise_for_status()
    client_id = response.json()["credentials"]["clientId"]
    client_secret = response.json()["credentials"]["clientSecret"]

    # Write to secrets.
    os.makedirs(SECRETS_DIR, exist_ok=True)
    with open(os.path.join(SECRETS_DIR, f"{name}-client-id"), "w") as f:
        f.write(client_id)

    with open(os.path.join(SECRETS_DIR, f"{name}-client-secret"), "w") as f:
        f.write(client_secret)

    print(f"Created principle: {name} ✔︎ ")
    print(f"Wrote client_id to {os.path.join(SECRETS_DIR, f'{name}-client-id')} ✔︎ ")
    print(f"Wrote client_secret to {os.path.join(SECRETS_DIR, f'{name}-client-secret')} ✔︎")


except HTTPError as e:
    print(f"Error: {e}")
    print(f"Response: {response.text}")
    print(f"Failed to create principle: {name}")
    exit(1)
