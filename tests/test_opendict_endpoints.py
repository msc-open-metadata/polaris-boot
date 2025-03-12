import requests
import dotenv
import os
import re

from requests.exceptions import HTTPError

def get_auth_token() -> str:
    dotenv.load_dotenv(".env")

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    # Prepare request data.
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "PRINCIPAL_ROLE:ALL"
    }

    response: requests.Response = requests.post("http://localhost:8181/api/catalog/v1/oauth/tokens", data=data)

    try:
        token = response.json()["access_token"]
        return token
    except HTTPError as e:
           print(f"Error: {e}")
           print(f"Response: {response.text}")
           exit(1)

def test_create_udo():
     token = get_auth_token()

     # Prepare request data.
     data = {
         "name": "AndreasFunc",
         "description": "Test UDO description",
         "type": "TEST"
     }

     headers = {
         "Authorization": f"Bearer {token}"
     }

     response: requests.Response = requests.post("http://localhost:8181/api/catalog/v1/udos", json=data, headers=headers)

     try:
         response.raise_for_status()
         print(f"Response: {response.text}")
     except HTTPError as e:
           print(f"Error: {e}")
           print(f"Response: {response.text}")
           exit(1)

def test_show_udo():
    return
