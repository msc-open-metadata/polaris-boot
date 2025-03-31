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
                "signature": "STRING",
                "return_type": "STRING",
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
        assert response.status_code in {501}


def test_create_function_udo():
    token = get_auth_token()

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    data = json.dumps(
        {
            "udo": {
                "type": "function",
                "name": "foo",
                "props": {
                    "args": {"arg1": "number", "arg2": "number"},
                    "language": "python",
                    "def": "def foo(arg1, arg2):\n    return arg1 + arg2",
                    "comment": "test fun",
                    "runtime": "3.12",
                    "client_version": "1",
                    "return_type": "number",
                    "signature": "foo(arg1: str, arg2: int) -> str"

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

    headers = {"Authorization": f"Bearer {token}"}

    response: requests.Response = requests.delete(
        "http://localhost:8181/api/opendic/v1/objects/platform_mappings", headers=headers
    )

    try:
        response.raise_for_status()
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.json()}")
        assert response.status_code in {501, 409}


def test_add_platform_mapping():
    token = get_auth_token()

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # data1 = json.dumps(
    #     {
    #         "createplatformmappingrequest": {
    #             "typeName": "and_func",
    #             "platformName": "snowflake",
    #             "syntax": "CREATE OR ALTER <type> <function_name>(<args>)\n    RETURNS <return_type>\n    LANGUAGE <language>\n    RUNTIME = <runtime>\n    PACKAGES = (<packages>)\n    HANDLER = '<name>'\n    AS $$\n<def>\n$$",
    #             "objectDumpMap": {
    #                 "args": {"type": "map", "format": "<key> <value>", "delimiter": ", "},
    #                 "packages": {"type": "list", "format": "'<item>'", "delimiter": ", "},
    #             },
    #         }
    #     }
    # )
    data = json.dumps(
        {
            "platformMapping": {
                "typeName": "function",
                "platformName": "snowflake",
                "syntax": "CREATE OR ALTER <type> <signature>\n    RETURNS <return_type>\n    LANGUAGE <language>\n    RUNTIME = <runtime>\n    HANDLER = '<name>'\n    AS $$\n<def>\n$$",
            }
        }
    )
    type = "function"
    platform = "snowflake"

    response: requests.Response = requests.post(
        f"http://localhost:8181/api/opendic/v1/objects/{type}/platforms/{platform}", headers=headers, data=data
    )

    try:
        response.raise_for_status()
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.json()}")
        assert response.status_code in {501, 409}
