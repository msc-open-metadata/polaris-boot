import os
from sys import argv

import requests
from requests.models import HTTPError

SECRETS_DIR = "./secrets"


def main():
    try:
        print(f"args: {len(argv)}")
        name = argv[1]
        token = argv[2]
    except Exception as e:
        print("Usage: ./create-princple.py <string:name> <string:access_token>")
        print(f"Error: {e}")
        exit(1)

    url = "http://localhost:8181/api/management/v1/principals"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"name": f"{name}", "type": "user"}

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
        if response.status_code == 401:
            print(f"Unauthorized. Check your access token: {token}")
            exit(1)
        if response.status_code == 409:
            print(f"Principal already exists: {name}")
            exit(0)


if __name__ == "__main__":
    main()
