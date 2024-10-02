from apis.post import router
from fastapi.testclient import TestClient
from auth.auth_handler import decodeJWT
from uuid import uuid4
from main import app  # assuming your FastAPI app is defined in main.py
from datetime import *
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import pytest
import json

client = TestClient(router)

test_jwt_tmp = None

test_CreatePScriptInput = {
    "post_id": 1
}

test_DeletePScriptInput = {
    "post_id": "1"
}


""" Manage post script test 1 """
def test_manage_pscript(client, test_jwt):
    response = client.post(
        "pscript",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePScriptInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # pscript 객체 확인
    assert response_json["post_id"] == test_CreatePScriptInput["post_id"]

# Manage post script test fail ( post_id가 없는 경우 )
async def test_managePScript_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("pscript", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to manage pscript"


""" Manage post script test 2 """
def test_manage_pscript(client, test_jwt):
    response = client.post(
        "pscript",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePScriptInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # pscript 객체 확인
    assert response_json["post_id"] == test_CreatePScriptInput["post_id"]

# Manage post script test fail ( post_id가 없는 경우 )
async def test_managePScript_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("pscript", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to manage pscript"


""" Create post script test """
def test_create_pscript(client, test_jwt):
    response = client.post(
        "pscript/create",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_CreatePScriptInput
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, dict)

    # pscript 객체 확인
    assert response_json["post_id"] == test_CreatePScriptInput["post_id"]

# Create post script test fail ( 잘못된 jwt )
async def test_CreatePScriptInput_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer wrong_jwt_token"}
        client.post("pscript/create", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create pscript"

# Create post script test fail ( post_id가 없는 경우 )
async def test_createp_script_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer {test_jwt_tmp['access_token']}"}
        client.post("pscript/create", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to create pscript"


""" Delete post script test """
def test_delete_pscript(client, test_jwt):
    response = client.request(
        method="DELETE",
        url="pscript/delete",
        headers={"Authorization": f"Bearer {test_jwt['access_token']}"},
        json=test_DeletePScriptInput
    )

    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list)

    # pscript 객체 확인
    for item in response_json:
        assert item["post_id"] == int(test_DeletePScriptInput["post_id"])

# Delete post script test fail ( 잘못된 jwt )
async def test_DeletePScriptInput_fail():
    with pytest.raises(HTTPException) as err:
        headers={"Authorization": f"Bearer wrong_jwt_token"}
        client.delete("pscript/delete", headers=headers)
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete pscript"

# Delete post script test fail ( post_id가 없는 경우 )
async def test_DeletePScriptInput_fail():
    with pytest.raises(HTTPException) as err:
        client.delete("pscript/delete")
    assert err.value.status_code == HTTP_400_BAD_REQUEST
    assert err.value.detail == "Failed to delete pscript"