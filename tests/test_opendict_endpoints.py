import json
import os

import dotenv
import requests
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
        "scope": "PRINCIPAL_ROLE:ALL",
    }

    response: requests.Response = requests.post("http://localhost:8181/api/catalog/v1/oauth/tokens", data=data)

    try:
        token = response.json()["access_token"]
        return token
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.text} ")
        exit(1)


def test_show_all_udos():
    token = get_auth_token()

    headers = {"Authorization": f"Bearer {token}"}

    response: requests.Response = requests.get("http://localhost:8181/api/opendic/v1/objects", headers=headers)

    try:
        response.raise_for_status()
        print(f"Response: {response.text}")
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.text}")
        assert response.status_code == 501


def test_show_function_udo():
    token = get_auth_token()

    headers = {"Authorization": f"Bearer {token}"}

    response: requests.Response = requests.get(
        "http://localhost:8181/api/opendic/v1/objects/function/", headers=headers
    )

    try:
        response.raise_for_status()
        print(f"Response: {response.text}")
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.text}")
        assert response.status_code == 501


def test_create_function_udo():
    token = get_auth_token()

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    data = json.dumps({
        "udo": {
            "type": "function",
            "name": "function",
            "props": {
                    "args": {
                        "arg1": "string",
                        "arg2": "number"
                    },
                    "language": "sql"
                }
        }
    })

    response: requests.Response = requests.post(
        "http://localhost:8181/api/opendic/v1/objects/function/", headers=headers, data=data
    )

    try:
        response.raise_for_status()
        print(f"Response: {response.text}")
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.text}")
        assert response.status_code == 501
