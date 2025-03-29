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
        print(f"Response: {response.json()}")
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.json()}")


def test_show_function_udo():
    token = get_auth_token()

    headers = {"Authorization": f"Bearer {token}"}

    response: requests.Response = requests.get(
        "http://localhost:8181/api/opendic/v1/objects/function/", headers=headers
    )

    try:
        response.raise_for_status()
        print(f"Response: {response.json()}")
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.json()}")

    assert response.status_code == 200


def test_define_function_udo():
    token = get_auth_token()

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    data = json.dumps(
        {
            "udoType": "function",
            "properties": {
                "args": "MAP",
                "language": "STRING",
                "def": "string",
                "comment": "string",
                "runtime": "string",
                "client_version": "int",
            },
        }
    )

    response: requests.Response = requests.post(
        "http://localhost:8181/api/opendic/v1/objects/", headers=headers, data=data
    )

    try:
        response.raise_for_status()
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.json()}")
        assert response.status_code in {501, 409}


def test_create_function_udo():
    token = get_auth_token()

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    data = json.dumps(
        {
            "udo": {
                "type": "function",
                "name": "foo",
                "props": {
                    "args": {"arg1": "string", "arg2": "number"},
                    "language": "python",
                    "def": "def foo(arg1, arg2):\n    return arg1 + arg2",
                    "comment": "test fun",
                    "runtime": "3.13",
                    "client_version": "1",
                },
            }
        }
    )

    response: requests.Response = requests.post(
        "http://localhost:8181/api/opendic/v1/objects/function/", headers=headers, data=data
    )

    try:
        response.raise_for_status()
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.json()}")
        assert response.status_code in {501, 409}


def test_drop_function_udo():
    token = get_auth_token()

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    data = json.dumps(
        {
            "udo": {
                "type": "function",
                "name": "foo",
                "props": {
                    "args": {"arg1": "string", "arg2": "number"},
                    "language": "python",
                    "def": "def foo(arg1, arg2):\n    return arg1 + arg2",
                    "comment": "test fun",
                    "runtime": "3.13",
                    "client_version": "1",
                },
            }
        }
    )

    response: requests.Response = requests.delete(
        "http://localhost:8181/api/opendic/v1/objects/function/foo", headers=headers, data=data
    )

    try:
        response.raise_for_status()
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.json()}")
        assert response.status_code in {501, 409}
