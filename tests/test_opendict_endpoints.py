import json
import os
import pprint

import dotenv
import requests
from requests.exceptions import HTTPError

"""
Polaris opendic end-2-end tests.
"""

EXAMPLE_PLATFORM_MAPPING = {
    "platformMapping": {
        "typeName": "function",
        "platformName": "snowflake",
        "syntax": "CREATE OR ALTER <type> <signature>\n    RETURNS <return_type>\n    LANGUAGE <language>\n    RUNTIME = <runtime>\n    HANDLER = '<name>'\n    AS $$\n<def>\n$$",
        "objectDumpMap": {
            "args": {
                "propType": "map",
                "format": "<key> <value>",
                "delimiter": ", ",
            },
            "packages": {"propType": "list", "format": "'<item>'", "delimiter": ", "},
        },
    }
}

EXAMPLE_UDO = {
    "udo": {
        "type": "function",
        "name": "foo",
        "props": {
            "args": {"arg1": "number", "arg2": "number"},
            "language": "python",
            "def": "def foo(arg1, arg2):\n    return arg1 + arg2",
            "comment": "test fun",
            "runtime": "3.12",
            "client_version": 1,
            "return_type": "int",
            "signature": "foo(arg1: str, arg2: int) -> str",
        },
    }
}


def pretty_print_test_result(test_name, response: requests.Response):
    """
    Pretty print test results including test name, status code and response.

    Args:
        test_name (str): The name of the test
        response (requests.Response): The HTTP response object
    """
    print("\n" + "=" * 80)
    print(f"TEST: {test_name}")
    print(f"STATUS CODE: {response.status_code}")
    print("-" * 80)
    print("RESPONSE:")

    try:
        # Pretty print the JSON response
        pprint.pprint(response.json(), indent=4, width=80)
    except ValueError:
        # In case the response is not JSON
        print(response.text)

    print("=" * 80)


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
        TOKEN = response.json()["access_token"]
        return TOKEN
    except HTTPError as e:
        print(f"Error: {e}")
        print(f"Response: {response.text} ")
        exit(1)


TOKEN = get_auth_token()


def test_001_define_function_udo():
    test_name = "test_001_define_function_udo()"

    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
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
    response: requests.Response = requests.post("http://localhost:8181/api/opendic/v1/objects/", headers=headers, data=data)
    pretty_print_test_result(test_name, response)

    assert response.status_code in {201, 409}
    if response.status_code == 409:
        assert "Type function already exists with schema" in response.json()["error"]["message"]


def test_002_show_all_udos():
    test_name = "test_002_show_all_udos()"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response: requests.Response = requests.get("http://localhost:8181/api/opendic/v1/objects", headers=headers)

    pretty_print_test_result(test_name, response)

    assert response.status_code == 200
    assert "function" in response.json()


def test_003_create_function_udo():
    test_name = "test_003_create_function_udo()"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = json.dumps(EXAMPLE_UDO)
    response: requests.Response = requests.post(
        "http://localhost:8181/api/opendic/v1/objects/function/", headers=headers, data=data
    )

    pretty_print_test_result(test_name, response)

    assert response.status_code in {201}


def test_004_create_duplicate_function_udo():
    test_name = "test_004_create_duplicate_function_udo()"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = json.dumps(EXAMPLE_UDO)
    response: requests.Response = requests.post(
        "http://localhost:8181/api/opendic/v1/objects/function/", headers=headers, data=data
    )

    pretty_print_test_result(test_name, response)

    assert response.status_code in {409}


def test_005_show_function_udo():
    test_name = "test_005_show_function_udo()"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    response: requests.Response = requests.get("http://localhost:8181/api/opendic/v1/objects/function/", headers=headers)

    pretty_print_test_result(test_name, response)

    assert isinstance(response.json(), list)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_006_add_platform_mapping():
    test_name = "test_006_add_platform_mapping()"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = json.dumps(EXAMPLE_PLATFORM_MAPPING)
    type = "function"
    platform = "snowflake"

    response: requests.Response = requests.post(
        f"http://localhost:8181/api/opendic/v1/objects/{type}/platforms/{platform}", headers=headers, data=data
    )

    pretty_print_test_result(test_name, response)

    assert response.status_code == 201

def test_007_add_duplicate_platform_mapping():
    test_name = "test_007_add_duplicate_platform_mapping()"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = json.dumps(EXAMPLE_PLATFORM_MAPPING)
    type = "function"
    platform = "snowflake"

    response: requests.Response = requests.post(
        f"http://localhost:8181/api/opendic/v1/objects/{type}/platforms/{platform}", headers=headers, data=data
    )

    pretty_print_test_result(test_name, response)

    assert response.status_code == 409


def test_008_show_all_mappings():
    test_name = "008_show_all_mappings"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response: requests.Response = requests.get("http://localhost:8181/api/opendic/v1/platforms", headers=headers)

    pretty_print_test_result(test_name, response)

    assert response.status_code in {200}
    assert len(response.json()) == 1


def test_009_show_snowflake_mappings():
    test_name = "009_show_snowflake_mappings"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response: requests.Response = requests.get("http://localhost:8181/api/opendic/v1/platforms/snowflake", headers=headers)

    pretty_print_test_result(test_name, response)

    assert response.status_code in {200}
    assert len(response.json()) == 1

def test_010_show_udo_mappings():
    test_name = "test_010_show_function_mappings"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    type:str = EXAMPLE_UDO["udo"]["type"]
    response: requests.Response = requests.get(f"http://localhost:8181/api/opendic/v1/objects/{type}/platforms", headers=headers)

    pretty_print_test_result(test_name, response)

    assert response.status_code in {200}
    assert len(response.json()) == 1

def test_011_get_udo_platform_mapping():
    test_name = "test_011_get_udo_platform_mapping"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    type:str = EXAMPLE_UDO["udo"]["type"]
    platform:str =EXAMPLE_PLATFORM_MAPPING["platformMapping"]["platformName"]
    response: requests.Response = requests.get(f"http://localhost:8181/api/opendic/v1/objects/{type}/platforms/{platform}", headers=headers)

    pretty_print_test_result(test_name, response)

    assert response.status_code in {200}



def test_00X_drop_function_udo():
    test_name = "00X_drop_function_udo"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response: requests.Response = requests.delete("http://localhost:8181/api/opendic/v1/objects/function", headers=headers)

    pretty_print_test_result(test_name, response)

    assert response.status_code in {200}


def test_OOY_drop_snowflake_mappings():
    test_name = "OOY_drop_snowflake_mappings"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response: requests.Response = requests.delete("http://localhost:8181/api/opendic/v1/platforms/snowflake", headers=headers)

    pretty_print_test_result(test_name, response)

    assert response.status_code in {200}

def test_00Z_drop_non_existent():
    test_name = "00Z_drop_non_existent"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response: requests.Response = requests.delete("http://localhost:8181/api/opendic/v1/objects/non_existent", headers=headers)

    pretty_print_test_result(test_name, response)

    assert response.status_code == 404
